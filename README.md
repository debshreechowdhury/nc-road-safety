# Beyond the Crash Count: Understanding Traffic Crash Severity

## Project Overview

Traffic crash counts tell us where and when crashes occur most often, but
frequency alone does not describe how serious their outcomes are.

This project explores traffic safety from two complementary perspectives:

1. **North Carolina geographic crash severity**, using official North Carolina
   Department of Transportation (NCDOT) crash records from 2021–2025.
2. **U.S. crash timing and road-user vulnerability**, using National Highway
   Traffic Safety Administration (NHTSA) Crash Report Sampling System (CRSS)
   data from 2016–2020.

The central data-storytelling idea is:

> **Crash frequency and crash severity are not the same thing.**

The project examines where crashes are concentrated, where serious outcomes
are more common among recorded crashes, when severe crashes occur, and how
injury severity differs across road-user groups.

The analyses are descriptive. They identify patterns and associations in
police-reported crash data but do not establish causal relationships or
measure individual crash risk per trip or mile traveled.

---

## Research Questions

The project addresses several related questions:

### North Carolina Geography and Severity

- Where are the largest numbers of crashes recorded across North Carolina?
- Which counties have higher rates of fatal or serious-injury outcomes among
  recorded crashes?
- Do counties with the highest crash volumes also have the highest
  serious-outcome rates?
- How do serious outcomes differ between rural-coded and municipal/city-coded
  crashes?
- Is county rural crash composition associated with serious-outcome rates?

### U.S. Crash Timing and Vulnerability

- At what times of day are crashes most common?
- Are the hours with the greatest crash volume also the hours with the highest
  severe-crash rates?
- Which road-user groups experience the highest serious or fatal injury rates
  among people involved in police-reported crashes?
- Do differences between road-user groups persist across years?
- How does late-night crash involvement relate to serious/fatal injury rates?

---

# Data Sources

The project uses two independent crash datasets. They should not be combined
into a single analytical dataset because they represent different populations,
time periods, sampling structures, and analytical purposes.

## 1. North Carolina Department of Transportation Crash Data

The North Carolina analysis uses the **NCDOT statewide crash dataset**.

The source data contain crash-level records from January 2021 onward. The
project restricts the main analysis to the five complete calendar years:

**2021–2025**

After filtering to complete years, the analysis contains approximately
**1.54 million recorded crashes** across all 100 North Carolina counties.

Important variables include:

- crash date and year
- county
- city / rural designation
- crash severity
- crash type
- fatalities and injury counts
- selected crash-related indicators

### Crash Severity

The NCDOT data use KABCO-style crash severity classifications.

For this project:

- **K** — fatal injury
- **A** — serious/disabling injury
- **B** — evident injury
- **C** — possible injury
- **O** — no injury/property-damage-only
- **U** — unknown severity

The project defines a **serious outcome** as a crash classified as either
**K or A**.

The primary county-level severity metric is:

> **Serious Outcome Rate = K+A crashes per 1,000 recorded crashes with known
> severity**

Records with unknown severity (`U`) are excluded from the denominator.

NCDMV crash-reporting documentation:

https://connect.ncdot.gov/business/DMV/DMV%20Documents/DMV-349%20Instructional%20Manual.pdf

NCDMV DMV-349 Code Sheets:

https://connect.ncdot.gov/business/DMV/DMV%20Documents/DMV-349%20Code%20Sheets.pdf

NCDOT crash-data resources:

https://ncdot.maps.arcgis.com/home/item.html?id=08ada689aca34927b0f78006fa885d36#overview

US Census Data:

https://www2.census.gov/geo/tiger/GENZ2025/shp/

### Geographic Boundary Data

County maps use the **2025 U.S. Census Bureau Cartographic Boundary county
file at 1:500,000 resolution**.

Only North Carolina counties (`STATEFP = 37`) are retained.

The Census data provide geographic polygons only. All crash statistics shown
on the maps are calculated from the NCDOT crash records.

See `data/external/README.md` for the exact boundary dataset source and local
file requirements.

---

## 2. NHTSA Crash Report Sampling System (CRSS), 2016–2020

The national analysis uses data from the **National Highway Traffic Safety
Administration (NHTSA) Crash Report Sampling System (CRSS)** for 2016–2020.

The files used in this project were obtained through the Kaggle
**US Traffic Accidents** dataset, which packages NHTSA CRSS records for these
years.

Dataset:

https://www.kaggle.com/datasets/jonbown/us-2020-traffic-accidents

CRSS is a nationally representative sample of police-reported motor-vehicle
crashes. Unlike the NCDOT dataset, CRSS is sample-based; therefore the national
analyses use the supplied CRSS sampling weights when estimating crash totals
and injury rates.

Three types of yearly files are used:

- `acc_YY.csv` — crash/accident-level records
- `pers_YY.csv` — person-level records
- `veh_YY.csv` — vehicle-level records

where `YY` ranges from `16` through `20`.

The crash-level analysis combines the annual accident files from 2016–2020.

The road-user vulnerability analysis joins:

- person records to accident records using `CASENUM`
- person records to vehicle records using `CASENUM + VEH_NO`

The person-level analysis uses the CRSS person weight (`WEIGHT`) when
calculating estimated counts and injury rates.

For the CRSS analyses:

- a severe crash is defined using `MAXSEV_IM` values 3 or 4
- a serious/fatal person injury is defined using `INJSEV_IM` values 3 or 4
- late night is defined as midnight through 5:59 a.m.
- motorcycle records are identified using `BDYTYP_IM` values 80–89

These definitions follow the variables and coding used in the project
notebooks.

---

# Analysis Workflow

The repository contains separate notebooks for the two analytical tracks.

## NCDOT North Carolina Analysis

### `notebooks/00_data_exploration.ipynb`

Performs the preliminary exploration and quality checks for the NCDOT data.

The notebook:

- loads data through the shared preprocessing pipeline
- restricts analysis to complete years 2021–2025
- examines dataset dimensions and columns
- evaluates missing values
- validates year coverage
- examines crash-severity distributions
- validates engineered serious-outcome features
- checks crash identifiers and dates
- calculates the statewide serious-outcome baseline

### `notebooks/01_geography_severity_analysis.ipynb`

Performs the North Carolina county-level geography and severity analysis.

The notebook:

- aggregates crashes by county
- calculates crash counts
- calculates known-severity counts
- calculates K+A serious-crash counts
- calculates serious-outcome rates
- compares county crash frequency with severity
- investigates county-level outliers
- compares rural-coded and municipal/city-coded crashes
- calculates county rural crash share
- examines rural crash share versus serious-outcome rate
- joins county metrics to U.S. Census geographic boundaries
- creates county-level choropleth maps

The analysis demonstrates why crash frequency and serious-outcome rate should
be considered separately.

---

## NHTSA CRSS Analysis

### `notebooks/01_data_exploration.ipynb`

Provides an initial inspection of the CRSS data files and the 2020 accident
dataset, including its structure, variables, descriptive statistics, and
available yearly accident/person/vehicle files.

### `notebooks/02_data_findings.ipynb`

Performs the crash-level temporal analysis using the CRSS accident files from
2016–2020.

The notebook:

- combines annual accident files
- defines serious/fatal crash outcomes
- engineers weekend, alcohol, darkness, rural, and daypart features
- uses CRSS case weights to estimate national crash totals
- calculates weighted severe- and fatal-crash rates
- compares crash volume by hour of day
- compares severe-crash rates by hour of day

This analysis extends the project's frequency-versus-severity theme to time:
the hours when crashes are most common are not necessarily the hours when
crashes are most likely to have severe outcomes.

### `notebooks/03_road_user_vulnerability.ipynb`

Extends the CRSS analysis from crashes to the people involved in them.

The notebook:

- combines person, accident, and vehicle records
- validates the joined person-level grain
- identifies major road-user groups
- distinguishes motorcyclists from enclosed-vehicle occupants
- calculates weighted serious/fatal injury rates
- compares pedestrians, motorcyclists, bicyclists, and enclosed-vehicle
  occupants
- checks whether observed disparities persist across 2016–2020
- compares late-night injury severity with other hours

The results describe injury severity **conditional on already being involved
in a police-reported crash**. They do not measure population risk, trip risk,
or risk per mile traveled.

---

# Reproducing the Analysis

## 1. Clone the Repository

```bash
git clone https://github.com/debshreechowdhury/nc-road-safety.git
cd nc-road-safety