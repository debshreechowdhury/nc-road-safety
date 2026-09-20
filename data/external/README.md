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