# ML Experiment Protocol

Copy this table for each experiment and complete the design before examining test results.

| Section | What to record |
| --- | --- |
| Question and hypothesis | The condition you will change, the expected effect, and the scope of the claim |
| Data | Source, license, version or hash, unit of splitting, and distribution in each split |
| Baselines | A naive baseline and a comparator relevant to prior work or practice |
| Method | Component under study, preprocessing, search space, compute budget, and random seeds |
| Evaluation | Primary metric, direction of improvement, minimum meaningful effect, secondary metrics, and how you will estimate uncertainty |
| Reproduction | Code revision, package and dataset versions, configuration, command, hardware, and artifact locations |
| Results and decision | Results by method and seed where applicable, differences from the baseline, failure analysis, and conclusions |

## Comparison rules

- Choose the unit of splitting based on what you want the model to generalize to. If several samples come from a single document, subject, or simulation case, keep that group in one split. For future-period prediction, split chronologically.
- Freeze the splits and fit data-dependent transformations on the training split. Use validation for feature, threshold, and hyperparameter selection. Examine test results after locking the method and evaluation criteria.
- Compare methods on the same splits, metrics, and evaluation conditions. Record the search budget and report runtime or compute costs when they are part of the claim.
- For stochastic training, specify the seeds in advance and report individual results alongside a summary. When estimating sampling uncertainty, use independent evaluation units appropriate to the study design.
- If the claim concerns the contribution of one component, vary that component in an ablation while holding other conditions fixed as far as the design allows. Qualify the claim when the results cannot distinguish the hypothesis from alternative explanations.

## Worked example

Does a word-frequency model outperform a majority-class predictor on synthetic texts about fluid flow and structures? Macro-F1 is the primary metric and accuracy is secondary. The splits are fixed and both baselines are deterministic, so this example needs no repeated training across seeds. The small dataset is designed to verify data loading, training, and evaluation.
