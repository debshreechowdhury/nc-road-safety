"""
Tests for crash-factor and temporal analysis.

The purpose of these tests is to verify analytical calculations using
small synthetic datasets where the expected answers can be determined
manually.

Do not use the full NCDOT CSV in unit tests.
"""

import pandas as pd
import pytest

from src.factor_analysis import (
    build_annual_summary,
    build_factor_summary,
)


# ---------------------------------------------------------------------
# TODO: Partner implementation
# ---------------------------------------------------------------------
#
# Add focused unit tests for the analysis functions.
#
# At minimum, tests should verify:
#
# 1. build_annual_summary()
#    - returns one row per year;
#    - calculates crash counts correctly;
#    - calculates K+A counts correctly;
#    - excludes U severity from the Serious Outcome Rate denominator.
#
# 2. build_factor_summary()
#    - counts only crashes where the selected factor is True;
#    - calculates factor-specific K+A counts correctly;
#    - excludes U severity from the denominator;
#    - calculates the severity multiplier against the statewide baseline.
#
# Use a small synthetic DataFrame so expected results can be calculated
# manually.
#
# Additional edge-case tests are encouraged.