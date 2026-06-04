# Changelog

## Unreleased

- Reframed the repository around the ATS 2022 abstract DOI
  `10.1164/ajrccm-conference.2022.205.1_MeetingAbstracts.A4996`.
- Added `llms.txt`, `CITATION.cff`, data dictionaries, dependency files, and a
  reproduction guide.
- Restored the missing historical HCO3 workbook loader and patient-record model
  expected by `DataAnalysis.py`.
- Added CLI input/output arguments and routed generated outputs under ignored
  output directories.
- Corrected a legacy loop/opiate exclusion getter mismatch in `RecordsDb.py`.
- Archived historical aggregate outputs in the
  `legacy-ats2022-aggregate-outputs-2026-06-04` release before removing
  generated artifacts and IDE files from the branch tip.
