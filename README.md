# Bari-CPAP

[![ATS abstract](https://img.shields.io/badge/ATS%202022-A4996-blue)](https://doi.org/10.1164/ajrccm-conference.2022.205.1_MeetingAbstracts.A4996)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](requirements.txt)

Legacy Python analysis for a University of Utah bariatric surgery cohort
examining CPAP use, serum bicarbonate trajectories, and suspected obesity
hypoventilation syndrome (OHS). The repository is associated with the ATS 2022
abstract **"Changes in Bicarbonate in Patients at Risk for Obesity
Hypoventilation Undergoing Bariatric Surgery"**.

This is a public code/documentation repository. It does not include restricted
patient-level clinical source workbooks.

## Links And Identifiers

| Item | Link |
| --- | --- |
| ATS abstract | https://doi.org/10.1164/ajrccm-conference.2022.205.1_MeetingAbstracts.A4996 |
| Public talk page | https://reblocke.github.io/talks/2022-HCO3-BARIATRIC |
| Repository | https://github.com/reblocke/Bari-CPAP |
| Machine-readable index | [llms.txt](llms.txt) |
| Historical aggregate output release | https://github.com/reblocke/Bari-CPAP/releases/tag/legacy-ats2022-aggregate-outputs-2026-06-04 |

## Authors, Funding, And Disclosures

| Contributor | Role | Affiliation |
| --- | --- | --- |
| Brian W. Locke, MD | Abstract author, repository maintainer | University of Utah |
| Conrad Addison, MD | Abstract author | University of Utah |
| Somya Mishra, MD | Abstract author | University of Utah |
| Krishna M. Sundar, MD | Abstract author | University of Utah |

Funding and conflict-of-interest details were not reported in the current public
repository materials. Use the ATS abstract record as the source of record if
additional disclosure metadata are needed.

## Data Access

The source workbooks are restricted clinical data and are not public:

```text
data/private/BARI_SLEEP_CPAP_COMPLIANCE_092619.xlsx
data/private/Bari HCO3 10-30-21-working.xlsx
```

Use local, de-identified or institutionally approved copies with the same sheet
and column structure. Do not commit raw workbooks, row-level derived files,
identifiers, or generated outputs.

Variable, workbook, and output documentation is in
[data_dictionary.md](data_dictionary.md) and [data_dictionary.csv](data_dictionary.csv).

## Repository Layout

```text
DataAnalysis.py        Legacy analysis entry point and figure/table workflow
AccessDb.py            Workbook loader and patient-database construction
RecordsDb.py           Legacy patient record/dataframe model
WriteDb.py             Historical openpyxl scratch script
tests/                 Synthetic no-PHI smoke tests and fixtures
REPRODUCING.md         Reproduction guide for local workbooks
CITATION.cff           Machine-readable citation metadata
llms.txt               Machine-readable repository summary
```

Generated outputs are written under `outputs/legacy-python/` by default and are
ignored by git. Historical aggregate outputs formerly tracked in the repository
are archived in the release linked above.

## Quick Start

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
python DataAnalysis.py --input-dir data/private --output-dir outputs/legacy-python
```

The script expects workbook sheet name `Sheet 1` in both input files. It writes
aggregate summary tables, a run log, and legacy figures under the selected
output directory.

## Dependencies

| Dependency | Use |
| --- | --- |
| `pandas`, `openpyxl` | Excel loading and dataframe outputs |
| `matplotlib`, `seaborn` | Legacy figures |
| `scipy`, `statsmodels` | Statistical summaries/tests used by legacy code |
| `python-dateutil` | Date arithmetic for age and timing variables |
| `pytest` | Synthetic-workbook smoke tests |

## Citation

Please cite the ATS abstract and the repository commit or release used:

> Locke BW, Addison C, Mishra S, Sundar KM. Changes in bicarbonate in patients
> at risk for obesity hypoventilation undergoing bariatric surgery. American
> Journal of Respiratory and Critical Care Medicine. 2022;205(Supplement_1):A4996.
> doi:[10.1164/ajrccm-conference.2022.205.1_MeetingAbstracts.A4996](https://doi.org/10.1164/ajrccm-conference.2022.205.1_MeetingAbstracts.A4996)

See [CITATION.cff](CITATION.cff) for structured metadata.

## License

Code and author-owned repository documentation are MIT licensed. Restricted
clinical data, generated row-level outputs, third-party materials, and publisher
pages are excluded from the repository license.

## Contact

Maintainer: Brian W. Locke (`@reblocke`; ORCID
[`0000-0002-3588-5238`](https://orcid.org/0000-0002-3588-5238)). Use GitHub
issues or pull requests for repository-specific questions.
