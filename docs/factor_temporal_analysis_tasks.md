# Factor and Temporal Analysis — Contributor Guide

## Goal

The task is to investigate how North Carolina crash frequency and
serious crash outcomes vary over time and across recorded crash
characteristics.

The project intentionally provides the analytical questions and shared
metric definitions while leaving implementation and visualization
choices flexible.

## Primary Deliverables

1. Annual crash summary for 2021-2025.
2. Crash-factor summary using the shared NCDOT factor columns.
3. At least one annual trend visualization.
4. A frequency-versus-severity visualization.
5. Unit tests for the analysis functions.
6. A short written summary in `docs/factor_findings.md`.

## Shared Code

Please use:

- `src.preprocessing.load_crash_data()`
- definitions in `src.config`
- metric functions in `src.metrics`

Avoid changing shared preprocessing or metric definitions unless a
problem is identified and discussed with the team first.

## Suggested Workflow

Load the standardized dataset:

    from src.preprocessing import load_crash_data

    df = load_crash_data()

Then develop and test the functions in:

    src/factor_analysis.py

After the analytical summaries are working, build visualizations in:

    src/factor_visualizations.py

## Flexibility

The TODO sections describe the minimum expected output rather than a
required implementation.

You may:

- restructure internal helper functions;
- add useful descriptive metrics;
- choose alternative chart types;
- improve naming or documentation;
- add additional tests;
- investigate interesting patterns discovered during analysis.

Please preserve the project's shared definitions of serious crashes and
the Serious Outcome Rate so results remain comparable with the geographic
analysis.

## Before Opening a Pull Request

Run:

    python -m pytest

Confirm all tests pass.

Run the factor analysis against the real dataset and inspect the
resulting summaries and figures.

Document the main findings and limitations in:

    docs/factor_findings.md

Then open a pull request from:

    feature/factor-temporal-analysis

into:

    main