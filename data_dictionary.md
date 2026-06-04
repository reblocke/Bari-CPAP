# Data Dictionary

This dictionary documents the restricted input workbooks, derived analysis
fields, and generated outputs for the legacy Bari-CPAP Python workflow. The
machine-readable companion is [data_dictionary.csv](data_dictionary.csv).

## Restricted Source Workbooks

| Workbook | Required sheet | Public status |
| --- | --- | --- |
| `BARI_SLEEP_CPAP_COMPLIANCE_092619.xlsx` | `Sheet 1` | Restricted clinical source data |
| `Bari HCO3 10-30-21-working.xlsx` | `Sheet 1` | Restricted clinical source data |

These workbooks should be supplied locally under `data/private/`. Do not commit
raw workbooks or row-level derived outputs.

## Required Outcome Workbook Columns

The outcomes workbook is parsed by header label. Required labels include
`PAT_ID`, `BARI_SURGERY_DATE`, `HEIGHT_CM_DOS`, the longitudinal
`WEIGHT_KG_*` fields, `Pre-op date`, `HCO3 pre-op`, `sCr pre-op`, longitudinal
`HCO3 *` fields, `Sex`, `DOB`, `CCI_SCORE`, and medication exclusion flags. The
legacy source label `Exlusion Loop` is intentionally documented with its
original spelling because the parser expects that text.

## Required Compliance Workbook Columns

The compliance workbook is parsed by fixed column position:

| Column | Meaning |
| --- | --- |
| A | Patient identifier used for workbook join |
| B | Download date |
| F | Percent of days with at least 4 hours of CPAP use |
| G | Number of days in the compliance report |
| Q | Diagnostic AHI |
| S | Diagnostic AHI date |

## Derived Fields

The workflow creates a legacy dataframe with sequential row indices rather than
source MRNs. Key derived variables include:

| Field | Definition |
| --- | --- |
| `Avg Compliance` | Weighted average percent of days with CPAP use at least 4 hours |
| `Days Comp Records` | Total days represented by compliance downloads |
| `Max Weight Loss` | Surgery weight minus lowest observed follow-up weight |
| `Weight Regain` | Last observed weight minus lowest observed weight |
| `Max Weight Loss Pct` | Percent loss from surgery weight to nadir |
| `Mean HCO3 Post Op` | Mean postoperative bicarbonate across available follow-up windows |
| `All HCO3 Below 25` | Whether all postoperative bicarbonate values are below 25 mEq/L |

## Generated Outputs

The canonical command writes generated files to `outputs/legacy-python/`:

```bash
python DataAnalysis.py --input-dir data/private --output-dir outputs/legacy-python
```

Outputs include local row-level workbooks (`full_output.xlsx`, `output.xlsx`),
aggregate describe tables, run logs, and legacy PNG figures. Generated outputs
are ignored by git. Historical aggregate outputs formerly tracked in the
repository are archived in the `legacy-ats2022-aggregate-outputs-2026-06-04`
release.

## Review Flags

- Exact source definitions for `CCI_SCORE` and some clinical timing windows are
  inferred from code and should be reviewed before scientific refactoring.
- Source workbooks may contain identifiers or date fields; generated row-level
  outputs remain local-only.
- This pass preserves the legacy analysis logic and documents uncertainty
  rather than redefining variables.
