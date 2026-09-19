"""
Project-wide configuration.

This module contains file paths, analysis settings, and shared column
definitions used across the project.

Keeping these values in one place helps ensure that both feature branches
use the same dataset, analysis period, and variable definitions.
"""

from pathlib import Path


# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

# Repository root directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

FIGURES_DIR = PROJECT_ROOT / "figures"

# Expected local name of the downloaded NCDOT crash dataset.
RAW_DATA_PATH = RAW_DATA_DIR / "nc_crashes.csv"


# ---------------------------------------------------------------------
# Analysis period
# ---------------------------------------------------------------------

# The NCDOT export contains partial data for 2026.
# To make year-to-year comparisons fair, the primary analysis is
# restricted to the five complete calendar years 2021–2025.
FULL_YEARS = [2021, 2022, 2023, 2024, 2025]


# ---------------------------------------------------------------------
# Crash severity definitions
# ---------------------------------------------------------------------

# NCDOT crash-severity categories used in this project.
#
# K = Fatal injury
# A = Serious / disabling injury
# B = Evident injury
# C = Possible injury
# O = No injury / property-damage-only crash
# U = Unknown severity
#
# Our primary outcome is a "serious crash," defined as K or A.
SERIOUS_SEVERITIES = ["K", "A"]


# ---------------------------------------------------------------------
# Crash-factor variables
# ---------------------------------------------------------------------

# Human-readable factor names mapped to the corresponding columns
# in the NCDOT dataset.
#
# These variables are used by the factor-analysis feature branch.
FACTOR_COLUMNS = {
    "Alcohol Related": "AlcRelated",
    "Drug Related": "DrugRelated",
    "Speed Related": "SpeedRelated",
    "Distracted Driver": "DistrDriver",
    "Drowsy Driver": "DrowsyDriver",
    "Animal Crash": "AnimalCrash",
    "Older Driver": "OlderDrvrInvolved",
    "Teen Driver": "TeenDrvrInvolved",
    "Unbelted Crash": "UnbeltedCrash",
    "Motorcycle Involved": "MotorcycleInvolved",
    "Heavy Truck Involved": "HvyTruckInvolved",
    "Pedestrian Involved": "PedInvolved",
    "Bicycle Involved": "BikeInvolved",
}


# ---------------------------------------------------------------------
# Columns required by the shared preprocessing pipeline
# ---------------------------------------------------------------------

REQUIRED_COLUMNS = [
    "Crash_ID",
    "Date",
    "Year",
    "Month",
    "County",
    "City",
    "Division",
    "MPORPO",
    "CrshSeverity",
    "NumFatalities",
    "NumAInjuries",
    "NumBInjuries",
    "NumCInjuries",
    "CrashType",
    *FACTOR_COLUMNS.values(),
]