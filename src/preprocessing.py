"""
Shared preprocessing utilities for the North Carolina crash dataset.

This module is responsible only for transformations that are required
by both project feature branches.

It intentionally does NOT contain geography-specific analysis or
crash-factor-specific analysis. Those will be implemented independently
in separate feature branches.

Main responsibilities
---------------------
1. Load the raw NCDOT CSV.
2. Validate that required columns exist.
3. Parse dates.
4. Restrict the primary analysis to complete years (2021–2025).
5. Create shared outcome features.
6. Standardize Y/N crash-indicator columns.
7. Create a simple rural-versus-municipal classification.
"""

import pandas as pd
from pathlib import Path

from src.config import (
    FACTOR_COLUMNS,
    FULL_YEARS,
    RAW_DATA_PATH,
    REQUIRED_COLUMNS,
    SERIOUS_SEVERITIES,
)


def validate_columns(df: pd.DataFrame) -> None:
    """
    Confirm that the input dataset contains the columns required by
    the shared analysis pipeline.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw crash dataset.

    Raises
    ------
    ValueError
        If one or more expected columns are missing.

    Notes
    -----
    Failing early with a useful error message is preferable to allowing
    an analysis script to fail later with a less informative KeyError.
    """

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "The NCDOT crash dataset is missing required columns: "
            + ", ".join(missing_columns)
        )


def standardize_indicator_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert NCDOT Y/N indicator fields to pandas Boolean values.

    NCDOT stores many crash characteristics as the strings "Y" and "N".
    Boolean values make filtering and aggregation easier and reduce the
    risk of inconsistent comparisons later in the project.

    Missing or unexpected values remain missing rather than being
    automatically interpreted as False.

    Parameters
    ----------
    df : pandas.DataFrame
        Crash dataframe.

    Returns
    -------
    pandas.DataFrame
        Dataframe with standardized Boolean indicator columns.
    """

    df = df.copy()

    mapping = {
        "Y": True,
        "N": False,
    }

    for column in FACTOR_COLUMNS.values():
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .str.upper()
            .map(mapping)
            .astype("boolean")
        )

    return df


def add_shared_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features used by both analysis branches.

    Shared engineered features
    --------------------------
    is_fatal
        True when the crash severity code is K.

    is_serious
        True when crash severity is either K (fatal) or
        A (serious/disabling injury).

    area_type
        Broad geographic classification based on the NCDOT `City`
        field:

        - "Rural" when City == "Rural"
        - "Municipal/City" when another municipality is recorded
        - "Unknown" when City is missing

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    df = df.copy()

    # Normalize severity text before constructing outcomes.
    df["CrshSeverity"] = (
        df["CrshSeverity"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    df["is_fatal"] = df["CrshSeverity"].eq("K")

    df["is_serious"] = df["CrshSeverity"].isin(
        SERIOUS_SEVERITIES
    )

    # Create a broad geographic classification from the NCDOT City field.
    #
    # NCDOT uses the literal value "Rural" for crashes that are not
    # associated with a municipality. Other non-missing City values are
    # treated as municipal/city records. Missing values remain "Unknown".
    city_clean = df["City"].astype("string").str.strip()

    df["area_type"] = "Unknown"

    df.loc[
        city_clean.notna() & city_clean.ne("Rural"),
        "area_type"
    ] = "Municipal/City"

    df.loc[
        city_clean.eq("Rural").fillna(False),
        "area_type"
    ] = "Rural"

    return df


def load_crash_data(
    path=RAW_DATA_PATH,
    complete_years_only: bool = True,
) -> pd.DataFrame:
    """
    Load and preprocess the NCDOT statewide crash dataset.

    Parameters
    ----------
    path : pathlib.Path or str, optional
        Path to the raw NCDOT CSV.

    complete_years_only : bool, default=True
        If True, retain only 2021–2025, which are complete calendar
        years in the downloaded dataset.

        Set this to False only when explicitly exploring partial-year
        2026 data.

    Returns
    -------
    pandas.DataFrame
        Cleaned crash-level dataframe ready for downstream analysis.

    Raises
    ------
    FileNotFoundError
        If the expected raw CSV does not exist.

    ValueError
        If required columns are missing.
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Raw NCDOT crash file was not found at: {path}\n"
            "Download the dataset and save it as "
            "'data/raw/nc_crashes.csv'."
        )

    df = pd.read_csv(
        path,
        low_memory=False,
    )

    validate_columns(df)

    # Parse crash dates. Invalid values are converted to NaT so they can
    # be inspected rather than silently producing incorrect dates.
    df["Date"] = pd.to_datetime(
        df["Date"],
        format="%m/%d/%Y",
        errors="coerce",
    )

    if complete_years_only:
        df = df[df["Year"].isin(FULL_YEARS)].copy()

    df = standardize_indicator_columns(df)
    df = add_shared_features(df)

    return df


if __name__ == "__main__":
    # Simple diagnostic entry point.
    #
    # Running:
    #
    #     python -m src.preprocessing
    #
    # provides a quick check that the local data file can be loaded
    # successfully before running feature-specific analysis.
    crash_df = load_crash_data()

    print("NCDOT crash dataset loaded successfully.")
    print(f"Rows available for analysis: {len(crash_df):,}")
    print(
        "Analysis years:",
        sorted(crash_df["Year"].dropna().unique().tolist()),
    )