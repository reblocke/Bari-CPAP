# Reproducing The Legacy Analysis

This repository does not include the restricted patient-level workbooks required
for the full analysis. To run the workflow, place approved local copies under:

```text
data/private/BARI_SLEEP_CPAP_COMPLIANCE_092619.xlsx
data/private/Bari HCO3 10-30-21-working.xlsx
```

Install dependencies and run from the repository root:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
python DataAnalysis.py --input-dir data/private --output-dir outputs/legacy-python
```

The script writes generated workbooks, figures, and a console log under the
selected output directory. Row-level generated files such as `full_output.xlsx`
and `output.xlsx` are local-only and should not be committed.

For a no-PHI smoke test, use the synthetic fixtures:

```bash
python -m pytest
python DataAnalysis.py --input-dir tests/fixtures --output-dir /tmp/bari-cpap-smoke
```

Historical aggregate outputs formerly tracked in the repository are archived at
https://github.com/reblocke/Bari-CPAP/releases/tag/legacy-ats2022-aggregate-outputs-2026-06-04.
They are retained for provenance and are not source workbooks.
