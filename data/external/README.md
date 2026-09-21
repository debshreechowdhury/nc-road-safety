# External Data

## U.S. Census County Boundaries

**Source:** U.S. Census Bureau — Cartographic Boundary Files  
**Dataset:** `cb_2025_us_county_500k.zip`  
**URL:** https://www2.census.gov/geo/tiger/GENZ2025/shp/

### Purpose

This dataset provides county boundary geometries used to create county-level
maps for the North Carolina crash analysis.

Only North Carolina counties (State FIPS `37`) are used. The county boundary
data is joined to the NCDOT crash summary by county name so that metrics such
as recorded crash count and serious-outcome rate can be visualized
geographically.

The boundary dataset provides geographic shapes only; crash statistics come
from the NCDOT crash dataset.

## Raw and Cleaned Data

Large raw datasets are not committed to this repository because they can be
downloaded from their original sources. All cleaned/analytical datasets are
generated programmatically from the raw files.

### NCDOT Crash Data
The North Carolina analysis uses the NCDOT Statewide Crash dataset. Download
instructions are provided in `data/raw/README.md`. Place the downloaded file at:

`data/raw/nc_crashes.csv`

The raw data are cleaned using `src/preprocessing.py`, which validates the
schema, parses dates, restricts the analysis to complete years 2021–2025,
standardizes indicators, and derives severity and geographic features.

### Census County Boundaries
County maps use the 2025 U.S. Census Cartographic Boundary county file.
Download instructions are provided in `data/external/README.md`. The boundary
data provide geographic shapes only; all crash metrics come from NCDOT data.

### NHTSA CRSS Data
The national analysis uses NHTSA CRSS 2016–2020 accident, person, and vehicle
files obtained from the Kaggle US Traffic Accidents dataset:
https://www.kaggle.com/datasets/jonbown/us-2020-traffic-accidents

The `acc_YY.csv`, `pers_YY.csv`, and `veh_YY.csv` files are combined, cleaned,
joined, and weighted directly within the CRSS notebooks.

No manually cleaned datasets are required. Following the documented download
steps and running the preprocessing code/notebooks reproduces the analytical
data used in this project.