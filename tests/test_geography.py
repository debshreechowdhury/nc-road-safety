"""Tests for reusable geographic analysis functions."""

import pandas as pd
import pytest

from src.geography import build_county_summary


def make_test_data():
    """Create a small synthetic two-county crash dataset."""

    return pd.DataFrame({
        "County": [
            "County A",
            "County A",
            "County A",
            "County A",
            "County B",
            "County B",
            "County B",
        ],
        "CrshSeverity": [
            "K",
            "A",
            "B",
            "U",
            "A",
            "C",
            "O",
        ],
        "is_serious": [
            True,
            True,
            False,
            False,
            True,
            False,
            False,
        ],
    })


def test_county_summary_returns_one_row_per_county():
    df = make_test_data()

    summary = build_county_summary(df)

    assert len(summary) == 2
    assert set(summary["County"]) == {"County A", "County B"}


def test_county_summary_counts_crashes_correctly():
    df = make_test_data()

    summary = build_county_summary(df)

    county_a = summary.loc[
        summary["County"] == "County A"
    ].iloc[0]

    assert county_a["crash_count"] == 4
    assert county_a["known_severity_count"] == 3
    assert county_a["serious_crash_count"] == 2


def test_county_summary_excludes_unknown_severity_from_rate():
    df = make_test_data()

    summary = build_county_summary(df)

    county_a = summary.loc[
        summary["County"] == "County A"
    ].iloc[0]

    # County A:
    # K + A = 2 serious crashes
    # K + A + B = 3 known-severity crashes
    #
    # 2 / 3 * 1000 = 666.67

    assert county_a["serious_rate_per_1000"] == pytest.approx(
        666.67,
        rel=1e-3,
    )