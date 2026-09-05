# AGENTS

## Project Purpose
This is a public legacy Python repository for the ATS 2022 bariatric surgery /
suspected obesity hypoventilation bicarbonate analysis. The public citation
target is DOI `10.1164/ajrccm-conference.2022.205.1_MeetingAbstracts.A4996`.

## Data Safety
- Treat all source workbooks under `data/private/` as restricted clinical data.
- Do not commit raw workbooks, row-level derived outputs, identifiers, local
  exports, private drafts, or publisher-formatted text/PDFs.
- Historical aggregate outputs are archived in the GitHub release
  `legacy-ats2022-aggregate-outputs-2026-06-04`; do not re-add them to the
  default branch.
- Keep generated outputs under ignored `outputs/` paths.

## Workflow
Run from the repository root:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
python DataAnalysis.py --input-dir data/private --output-dir outputs/legacy-python
```

Use `tests/fixtures/` for synthetic no-PHI smoke tests. The default workbook
sheet name is `Sheet 1` for both required inputs.

## Maintenance Rules
- Preserve the recognizable legacy workflow in `DataAnalysis.py`, `AccessDb.py`,
  and `RecordsDb.py` unless the user explicitly asks for a scientific refactor.
- Keep `README.md`, `llms.txt`, `CITATION.cff`, and the data dictionaries in
  sync when citation, data, or run-path details change.
- Validate `CITATION.cff` after citation edits.
- Mark inferred dictionary definitions as `needs_review` rather than guessing.

## Verification Before Publishing
For documentation-only edits, check affected references and `git diff --check`. For analysis-code or input-contract changes, run the tests and synthetic smoke below; they do not establish restricted-data reproduction. Use a fresh smoke output directory if the example destination already contains work.

```bash
python -m pytest
python DataAnalysis.py --input-dir tests/fixtures --output-dir /tmp/bari-cpap-smoke
git diff --check
```

Also run static searches for hard-coded local paths, stale conference-year wording,
tracked generated outputs, `.idea/`, and private workbook names outside
documentation or `.gitignore`.
