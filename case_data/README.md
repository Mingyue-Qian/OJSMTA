# Synthetic case data for joint CUA maintenance and task allocation

This repository provides the numerical inputs and experiment protocols for **Joint Optimization of Selective Maintenance and Task Allocation for a Carrier Unmanned Aircraft Fleet under Multi-Wave Sorties**, by Mingyue Qian, Lei Wang and Xinwei Wang. This data snapshot was prepared on 2 November 2026 for the manuscript revision.

The data are **manually specified synthetic planning instances**. They are not flight records, measurements or statistically calibrated estimates of a real carrier aircraft fleet. Results are model expectations. Scheduling a task does not imply an observed successful mission or probability-one success.

## Files

- `raw/`: five original Excel workbooks, copied without changing their bytes.
- `csv/`: one UTF-8 CSV per worksheet, retaining the title and header rows.
- `json/`: the same worksheet grids in JSON; null denotes an empty cell.
- `metadata/cases.json`: worksheet meanings, units, state order and original workbook SHA-256 values.
- `config/`: task subsets, seeds, budgets, formation membership, wave releases and scenario overrides.
- `reported_results/`: archived algorithm-comparison and joint/two-stage summaries, and all 100 new weight-sensitivity run records with their aggregate statistics.
- `validation/`: numerical input checks and feasibility/budget checks for the new weight experiment.
- `SHA256SUMS.txt`: checksums for every distributed file except the checksum list itself.
- `validate_cases.py`: standard-library checks for file integrity, probability rows, task subsets and wave releases.

The five workbooks have numerically identical base sheets `Sheet1`–`Sheet14`. The multi-wave workbook also preserves its additional worksheets. The low-health reallocation case is defined by the explicit **runtime overrides** in `config/deferred_task_reallocation.json`; the similarly named workbook alone does not define those overrides.

## Experiments and task subsets

| Experiment | Tasks | Runs or seed | Budget |
| --- | --- | --- | --- |
| Illustrative single-wave schedule | IDs 1–60 | seed 42 | 10,000 evaluations |
| Six-algorithm comparison | IDs 1–40 | 20 paired seeds 2000–2019 | 10,000 per algorithm and run |
| Joint versus two-stage comparison | IDs 1–40 | 20 paired seeds 8100–8119 | 10,000 per strategy and run; two stages receive 5,000 each |
| Normal multi-wave case | IDs 1–60 in six recorded releases | base seed 42 | 10,000 per wave |
| Deferred-task reallocation case | same 60 IDs and releases | base seed 42 | 10,000 per wave |
| Weight sensitivity | IDs 1–60 | 20 paired seeds 9200–9219 for each of five schemes | 10,000 per scheme and run |

The Table 4 comparison and joint/two-stage numerical summaries come from the archived **40-task** experiments. They must not be confused with the illustrative 60-task Gantt schedule or the new 60-task weight study. One additional isolated serial timing observation per algorithm uses seed 2000; these timings do not estimate runtime variability.

All weight schemes sum to one analytically. Scheme A is (0.4, 0.3, 0.2, 0.1). B and C reduce the raw task-benefit or health-benefit coefficient by 0.1; D and E increase the raw synchronization or maintenance-cost coefficient by 0.1. Each raw vector is then divided by its sum. These are illustrative preferences, not empirically elicited optimal weights. The CSV reports both each scheme's own weighted fitness and a common-reference score; scores computed with different preference vectors are not the same utility scale.

## Data conventions

There are ten aircraft, four subsystems (DTC, FCN, COM, NVG), five health states and five maintenance choices. State 1 is worst and absorbing under degradation; state 5 is best. Maintenance choice 1 is no maintenance and choice 5 is perfect restoration. State probabilities are row vectors, and maintenance restoration matrices are row-stochastic. The implemented CTMC allows adjacent downward transitions and integrates Weibull-density-based exposure; the specified Weibull parameter time unit is **hour**, while schedule calculations use seconds. Maintenance durations in the source workbook are minutes and are converted by the evaluator. Locations are kilometres and maintenance expenditures are CNY.

`Sheet1`–`Sheet4` contain initial subsystem probabilities; `Sheet5`–`Sheet8` contain aircraft-specific Weibull parameters; `Sheet9` contains maintenance costs and durations; `Sheet10` contains task requirements, durations and locations; `Sheet11` contains benefit inputs; `Sheet12` contains health-state utility weights; `Sheet13` contains task-class capacities; and `Sheet14` contains maintenance recovery probability matrices. The first two rows of these sheets are titles and headers, not observations. Aircraft-specific scale parameters are already recorded in the workbooks; do not apply the manuscript's scale multiplier a second time.

The stress case shortens the maintenance window from 120 to 60 minutes, sets all four subsystem distributions of formation A to (0, 0.8, 0.2, 0, 0), and requires state 4 in every subsystem for tasks 3 and 6. Other base data and the wave release list remain fixed. The exact machine-readable overrides and full configuration are provided in `config/`.

## Verification

Run `python validate_cases.py` from this folder. No third-party packages are required. The script checks checksums, the 200 initial-state probability rows and 500 recovery-matrix rows across the five workbooks' JSON exports, the shared base sheets, task subsets, 60 unique wave releases, and the new weight-study seeds and evaluation counts. It also checks that CSV and JSON grids agree. These checks establish input consistency; they do not independently reproduce the optimizer's numerical search.

Original workbooks, exported inputs and protocols permit inspection and reconstruction of each stated instance. This release does not claim to include the full optimizer source or an independently executed replication. No operationally collected aircraft data are included.
