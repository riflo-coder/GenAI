# GenAI

A framework for reproducible machine learning experiments. The existing notebook is available in [quickstarts/](quickstarts/).

## Run the first experiment

From the repository root, use Python 3.10 or later. The example uses the Python standard library.

```sh
python -m research.run --config configs/text_baseline.json --split validation --output runs/text-validation.json
```

The example fits a multinomial Naive Bayes classifier and a majority-class baseline on the same synthetic training split, then evaluates both on the validation split. The JSON output records sample counts, accuracy, macro-F1, predictions for each sample, the configuration, data and code hashes, the Python version, and the Git revision when available. The synthetic data is intended to verify the experiment workflow.

After freezing the method and evaluation criteria, run the final evaluation with `--split test --output runs/text-test.json`. Use a new output path for each run.

## Start a new study

1. Fill out the [experiment protocol](docs/research-protocol.md) with the question, hypothesis, baselines, primary metric, and success criteria.
2. Record the data source, version, license, and unit of splitting. Fit data-dependent preprocessing on the training split.
3. Run the baselines, select methods on the validation split, and evaluate the final method on the test split. Report variation across seeds for stochastic training.
4. Save the configuration and artifact references. Interpret the results, including negative findings.

| Path | Contents |
| --- | --- |
| `docs/research-protocol.md` | Experiment template and evaluation protocol |
| `configs/text_baseline.json` | Example configuration |
| `data/text_fixture.csv` | Synthetic dataset with fixed splits |
| `research/run.py` | Baseline training and evaluation |
| `runs/` | Local JSON results |
