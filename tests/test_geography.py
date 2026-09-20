"""Tests for reusable geographic analysis functions."""

import pandas as pd
import pytest

from src.geography import (
    build_county_summary,
    prepare_county_geodata,
    validate_county_coverage,
)

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
        "area_type": [
            "Rural",
            "Rural",
            "Municipal/City",
            "Municipal/City",
            "Rural",
            "Municipal/City",
            "Municipal/City",
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

def test_county_summary_calculates_rural_share():
    df = make_test_data()

    summary = build_county_summary(df)

    county_a = summary.loc[
        summary["County"] == "County A"
    ].iloc[0]

    assert county_a["rural_crash_count"] == 2
    assert county_a["rural_crash_share"] == pytest.approx(0.5)

def test_validate_county_coverage_accepts_expected_count():
    summary = pd.DataFrame({
        "County": ["A", "B"]
    })

    validate_county_coverage(
        summary,
        expected_counties=2,
    )


def test_validate_county_coverage_rejects_missing_county():
    summary = pd.DataFrame({
        "County": ["A"]
    })

    with pytest.raises(ValueError):
        validate_county_coverage(
            summary,
            expected_counties=2,
        )

def test_prepare_county_geodata_matches_counties():
    boundaries = pd.DataFrame({
        "NAME": ["County A", "County B"],
        "geometry": ["geometry_a", "geometry_b"],
    })

    summary = pd.DataFrame({
        "County": ["County A", "County B"],
        "crash_count": [100, 200],
        "serious_rate_per_1000": [20.0, 30.0],
    })

    result = prepare_county_geodata(
        boundaries,
        summary,
    )

    assert len(result) == 2
    assert result["crash_count"].tolist() == [100, 200]


def test_prepare_county_geodata_rejects_unmatched_county():
    boundaries = pd.DataFrame({
        "NAME": ["County A", "County C"],
        "geometry": ["geometry_a", "geometry_c"],
    })

    summary = pd.DataFrame({
        "County": ["County A", "County B"],
        "crash_count": [100, 200],
    })

    with pytest.raises(ValueError):
        prepare_county_geodata(
            boundaries,
            summary,
        )

def test_prepare_county_geodata_matches_counties_case_insensitively():
    boundaries = pd.DataFrame({
        "NAME": ["McDowell", "Wake"],
        "geometry": ["geometry_a", "geometry_b"],
    })

    summary = pd.DataFrame({
        "County": ["Mcdowell", "Wake"],
        "crash_count": [100, 200],
        "serious_rate_per_1000": [20.0, 30.0],
    })

    result = prepare_county_geodata(
        boundaries,
        summary,
    )

    assert len(result) == 2
    assert result["crash_count"].tolist() == [100, 200]