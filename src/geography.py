"""
Reusable geographic analysis functions for the NC Road Safety project.

This module contains geographic aggregation logic used by the
geography/severity analysis notebook and downstream visualizations.

The functions in this module operate on data already standardized by
src.preprocessing.
"""

import pandas as pd

from src.metrics import (
    known_severity_crash_count,
    serious_crash_count,
    serious_rate_per_1000,
    severity_multiplier,
)


def build_county_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build county-level crash frequency and severity metrics.

    Parameters
    ----------
    df : pandas.DataFrame
        Preprocessed NCDOT crash data containing County, CrshSeverity,
        and is_serious.

    Returns
    -------
    pandas.DataFrame
        One row per county containing:

        - County
        - crash_count
        - known_severity_count
        - serious_crash_count
        - serious_rate_per_1000
        - severity_multiplier
        - rural_crash_count
        - rural_crash_share

    Notes
    -----
    Serious Outcome Rate represents K+A crashes per 1,000 recorded
    crashes with known severity.

    Severity multiplier compares each county's Serious Outcome Rate
    with the statewide Serious Outcome Rate.

    These metrics describe outcomes among recorded crashes. They are
    not exposure-adjusted measures of roadway crash risk.
    """
    statewide_rate = serious_rate_per_1000(df)

    records = []

    for county, county_df in df.groupby("County"):
        rural_crash_count = county_df["area_type"].eq("Rural").sum()

        records.append({
            "County": county,
            "crash_count": len(county_df),
            "known_severity_count": known_severity_crash_count(county_df),
            "serious_crash_count": serious_crash_count(county_df),
            "serious_rate_per_1000": serious_rate_per_1000(county_df),
            "severity_multiplier": severity_multiplier(
                county_df,
                statewide_rate,
            ),
            "rural_crash_count": int(rural_crash_count),
            "rural_crash_share": rural_crash_count / len(county_df),
        })

    return (
        pd.DataFrame(records)
        .sort_values("crash_count", ascending=False)
        .reset_index(drop=True)
    )

def prepare_county_geodata(
    county_boundaries,
    county_summary: pd.DataFrame,
    boundary_name_col: str = "NAME",
):
    """
    Join county-level crash metrics to North Carolina county boundaries.

    Parameters
    ----------
    county_boundaries
        GeoDataFrame containing one polygon per North Carolina county.

    county_summary : pandas.DataFrame
        County-level crash summary produced by build_county_summary().

    boundary_name_col : str, default="NAME"
        Column in the boundary dataset containing county names.

    Returns
    -------
    geopandas.GeoDataFrame
        County boundary geometries with crash-frequency, severity,
        and rural-composition metrics attached.

    Raises
    ------
    ValueError
        If required county-name columns are missing, county names are
        duplicated, or the geographic join does not match every county.

    Notes
    -----
    This function intentionally does not download geographic data.
    Boundary acquisition is handled separately so that the analysis
    remains explicit about its external data sources.
    """
    if boundary_name_col not in county_boundaries.columns:
        raise ValueError(
            f"Boundary name column '{boundary_name_col}' was not found."
        )

    if "County" not in county_summary.columns:
        raise ValueError(
            "county_summary must contain a 'County' column."
        )

    if county_boundaries[boundary_name_col].duplicated().any():
        raise ValueError(
            "County boundary data contains duplicate county names."
        )

    if county_summary["County"].duplicated().any():
        raise ValueError(
            "County summary contains duplicate county names."
        )

    # Create normalized county-name keys for a case-insensitive join.
    boundaries = county_boundaries.copy()
    summary = county_summary.copy()

    boundaries["_county_join_key"] = (
        boundaries[boundary_name_col]
        .astype("string")
        .str.strip()
        .str.casefold()
    )

    summary["_county_join_key"] = (
        summary["County"]
        .astype("string")
        .str.strip()
        .str.casefold()
    )

    county_geo = boundaries.merge(
        summary,
        on="_county_join_key",
        how="left",
        validate="one_to_one",
    )

    unmatched = county_geo.loc[
        county_geo["crash_count"].isna(),
        boundary_name_col,
    ].tolist()

    if unmatched:
        raise ValueError(
            "County boundary join failed for: "
            + ", ".join(map(str, unmatched))
        )

    county_geo = county_geo.drop(
        columns="_county_join_key"
    )

    return county_geo

def validate_county_coverage(
    county_summary: pd.DataFrame,
    expected_counties: int = 100,
) -> None:
    """
    Validate county coverage before geographic analysis.

    Parameters
    ----------
    county_summary : pandas.DataFrame
        Output from build_county_summary().

    expected_counties : int, default=100
        Expected number of North Carolina counties.

    Raises
    ------
    ValueError
        If the number of unique counties does not match the expected
        number or duplicate county rows are present.
    """
    if county_summary["County"].duplicated().any():
        raise ValueError(
            "County summary contains duplicate county rows."
        )

    county_count = county_summary["County"].nunique()

    if county_count != expected_counties:
        raise ValueError(
            f"Expected {expected_counties} counties, "
            f"but found {county_count}."
        )