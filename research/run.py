"""Train and evaluate deterministic text baselines on a fixed split."""

import argparse
import csv
import hashlib
import io
import json
import math
import platform
import re
import subprocess
from collections import Counter
from pathlib import Path


def tokenize(text):
    return re.findall(r"\b\w+\b", text.casefold())


def git_revision():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def load_split(dataset_bytes, split):
    reader = csv.DictReader(io.StringIO(dataset_bytes.decode("utf-8-sig"), newline=""))
    required = {"id", "split", "label", "text"}
    if not required.issubset(reader.fieldnames or ()):
        raise ValueError("Dataset must contain id, split, label, and text columns.")

    partitions = {"train": [], "validation": [], "test": []}
    ids = set()
    texts = set()
    for row in reader:
        sample_id = (row["id"] or "").strip()
        label = (row["label"] or "").strip()
        tokens = tuple(tokenize(row["text"] or ""))
        partition = row["split"]
        if not sample_id or not label or not tokens or partition not in partitions:
            raise ValueError(f"Invalid sample at CSV line {reader.line_num}.")
        if sample_id in ids or tokens in texts:
            raise ValueError(f"Duplicate sample ID or normalized text: {sample_id}.")
        ids.add(sample_id)
        texts.add(tokens)
        partitions[partition].append((sample_id, label, tokens))

    train = partitions["train"]
    evaluation = partitions[split]
    labels = sorted({label for _, label, _ in train})
    if len(labels) < 2 or {label for _, label, _ in evaluation} != set(labels):
        raise ValueError("Train and evaluation splits must contain the same two or more labels.")
    return train, evaluation, labels


def predict(train, evaluation, labels, alpha):
    class_counts = Counter(label for _, label, _ in train)
    word_counts = {label: Counter() for label in labels}
    for _, label, tokens in train:
        word_counts[label].update(tokens)
    vocabulary = set().union(*(counts.keys() for counts in word_counts.values()))
    log_priors = {label: math.log(class_counts[label] / len(train)) for label in labels}
    denominators = {
        label: sum(word_counts[label].values()) + alpha * len(vocabulary)
        for label in labels
    }
    majority = max(labels, key=class_counts.__getitem__)
    predictions = []
    for sample_id, expected, tokens in evaluation:
        observed = [token for token in tokens if token in vocabulary]
        scores = {
            label: log_priors[label]
            + math.fsum(
                math.log(word_counts[label][token] + alpha) - math.log(denominators[label])
                for token in observed
            )
            for label in labels
        }
        predictions.append({
            "id": sample_id,
            "expected": expected,
            "majority": majority,
            "naive_bayes": max(labels, key=scores.__getitem__),
        })
    return predictions


def metrics(predictions, method, labels):
    confusion = Counter((row["expected"], row[method]) for row in predictions)
    f1 = []
    for label in labels:
        true_positive = confusion[label, label]
        actual = sum(confusion[label, other] for other in labels)
        predicted = sum(confusion[other, label] for other in labels)
        f1.append(2 * true_positive / (actual + predicted))
    return {
        "accuracy": sum(confusion[label, label] for label in labels) / len(predictions),
        "macro_f1": math.fsum(f1) / len(labels),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", choices=("validation", "test"), default="validation")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        alpha = config["alpha"]
        if type(alpha) not in (int, float) or not math.isfinite(alpha) or alpha <= 0:
            raise ValueError("alpha must be a finite positive number.")
        dataset = args.config.parent / config["dataset"]
        dataset_bytes = dataset.read_bytes()
        train, evaluation, labels = load_split(dataset_bytes, args.split)
        predictions = predict(train, evaluation, labels, alpha)
        result = {
            "config": config,
            "dataset_sha256": hashlib.sha256(dataset_bytes).hexdigest(),
            "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "git_revision": git_revision(),
            "python_version": platform.python_version(),
            "evaluation_split": args.split,
            "sample_counts": {"train": len(train), args.split: len(evaluation)},
            "labels": labels,
            "metrics": {
                method: metrics(predictions, method, labels)
                for method in ("majority", "naive_bayes")
            },
            "predictions": predictions,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as output:
            json.dump(result, output, indent=2, allow_nan=False)
            output.write("\n")
    except (OSError, KeyError, ValueError, TypeError, OverflowError) as error:
        parser.error(str(error))
    print(json.dumps(result["metrics"], indent=2))


if __name__ == "__main__":
    main()
