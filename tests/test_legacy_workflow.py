from pathlib import Path

import pandas as pd

from AccessDb import AccessDatabase
from DataAnalysis import (
    compliance_data_sheet,
    compliance_dbLoc,
    outcome_data_sheet,
    outcome_dbLoc,
    run_analysis,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_access_database_loads_synthetic_workbooks():
    database = AccessDatabase(
        FIXTURE_DIR,
        compliance_dbLoc,
        compliance_data_sheet,
        outcome_dbLoc,
        outcome_data_sheet,
    )
    df = database.createDataFrame()

    assert len(df) == 3
    assert df["MRN"].tolist() == [1, 2, 3]
    assert df["Diag AHI"].notna().sum() == 3


def test_derived_hco3_weight_and_exclusion_fields():
    database = AccessDatabase(
        FIXTURE_DIR,
        compliance_dbLoc,
        compliance_data_sheet,
        outcome_dbLoc,
        outcome_data_sheet,
    )
    df = database.createDataFrame()
    first = df.iloc[0]
    excluded = df.iloc[2]

    assert first["Pre Op HCO3"] == 27
    assert first["6mo Delta HCO3"] == -3
    assert first["Mean HCO3 Post Op"] < 25
    assert bool(first["All HCO3 Below 25"]) is True
    assert first["Weight Regain"] == 8
    assert first["Max Weight Loss"] == 20
    assert bool(first["Loop Exclusion"]) is False
    assert bool(first["Opiate Exclusion"]) is False

    assert bool(excluded["Loop Exclusion"]) is True
    assert bool(excluded["Opiate Exclusion"]) is False


def test_data_analysis_cli_workflow_writes_expected_outputs(tmp_path):
    run_analysis(FIXTURE_DIR, tmp_path)

    expected = [
        "full_output.xlsx",
        "whole_cohort_output_stats.xlsx",
        "output_stats.xlsx",
        "persistent_OHS_output_stats.xlsx",
        "OHS_resolved_output_stats.xlsx",
        "output.xlsx",
        "figure_1_delta_HCO3.png",
        "figure_2_HCO3.png",
    ]
    for filename in expected:
        assert (tmp_path / filename).exists()

    output_df = pd.read_excel(tmp_path / "output.xlsx")
    assert not output_df.empty
