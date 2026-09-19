"""
Unit tests for the shared preprocessing and metric utilities.

These tests use a tiny synthetic dataframe rather than the full NCDOT
dataset. This allows collaborators and automated workflows to test core
logic without downloading the large raw data file.
"""

import pandas as pd
import pytest

from src.metrics import (
    serious_crash_count,
    serious_rate_per_1000,
    severity_multiplier,
)
from src.preprocessing import (
    add_shared_features,
    standardize_indicator_columns,
    validate_columns,
)
from src.config import FACTOR_COLUMNS, REQUIRED_COLUMNS


def build_sample_dataframe():
    """
    Create a minimal synthetic dataframe with the same core schema used
    by the project.
    """

    data = {
        column: [None, None, None, None]
        for column in REQUIRED_COLUMNS
    }

    data["Crash_ID"] = [1, 2, 3, 4]
    data["Date"] = [
        "01/01/2024",
        "01/02/2024",
        "01/03/2024",
        "01/04/2024",
    ]
    data["Year"] = [2024, 2024, 2024, 2024]
    data["Month"] = [1, 1, 1, 1]

    data["County"] = [
        "Wake",
        "Wake",
        "Durham",
        "Durham",
    ]

    data["City"] = [
        "Raleigh",
        "Rural",
        "Durham",
        "Rural",
    ]

    data["CrshSeverity"] = ["K", "A", "B", "O"]

    # Give every Y/N crash-factor column a valid default.
    for column in FACTOR_COLUMNS.values():
        data[column] = ["N", "Y", "N", "N"]

    return pd.DataFrame(data)


def test_validate_columns_accepts_expected_schema():
    df = build_sample_dataframe()

    # Should complete without raising an exception.
    validate_columns(df)


def test_validate_columns_rejects_missing_column():
    df = build_sample_dataframe().drop(columns=["County"])

    with pytest.raises(ValueError):
        validate_columns(df)


def test_serious_crash_feature():
    df = build_sample_dataframe()
    df = add_shared_features(df)

    # K and A are considered serious.
    assert df["is_serious"].tolist() == [
        True,
        True,
        False,
        False,
    ]


def test_area_type_feature():
    df = build_sample_dataframe()
    df = add_shared_features(df)

    assert df["area_type"].tolist() == [
        "Municipal/City",
        "Rural",
        "Municipal/City",
        "Rural",
    ]


def test_indicator_conversion():
    df = build_sample_dataframe()
    df = standardize_indicator_columns(df)

    assert bool(df.loc[0, "SpeedRelated"]) is False
    assert bool(df.loc[1, "SpeedRelated"]) is True


def test_serious_rate_per_1000():
    df = build_sample_dataframe()
    df = add_shared_features(df)

    # Two serious crashes among four total crashes:
    #
    # 2 / 4 * 1000 = 500
    assert serious_rate_per_1000(df) == 500.0


def test_serious_crash_count():
    df = build_sample_dataframe()
    df = add_shared_features(df)

    assert serious_crash_count(df) == 2


def test_severity_multiplier():
    df = build_sample_dataframe()
    df = add_shared_features(df)

    # Sample rate = 500 per 1,000.
    # If statewide baseline = 250 per 1,000,
    # multiplier should equal 2.
    result = severity_multiplier(
        df,
        statewide_rate_per_1000=250,
    )

    assert result == 2.0