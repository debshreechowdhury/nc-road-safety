# Notebooks

This directory contains exploratory notebooks used to understand the
NCDOT crash dataset and validate the shared project pipeline.

## `00_data_exploration.ipynb`

Provides the common preliminary exploration used by both project analysis
tracks, including:

- dataset dimensions and temporal coverage
- schema inspection
- missing-value assessment
- annual crash counts
- crash-severity distribution
- validation of engineered features
- basic data-quality checks
- statewide Serious Outcome Rate

Feature-specific analysis is intentionally kept out of this notebook.

Geographic/severity analysis and crash-factor/temporal analysis are
implemented independently in their respective feature branches.

Reusable preprocessing, feature engineering, and metric calculations
belong in `src/` rather than being implemented only inside notebooks.