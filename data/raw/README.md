# Raw Data

This directory is used for the original North Carolina traffic crash
dataset used in this project.

## Dataset Source

The project uses statewide crash data published by the
North Carolina Department of Transportation (NCDOT).

The data were downloaded from the NCDOT Statewide Crash Dashboard /
ArcGIS data source.

The downloaded export contains one record per reported crash and includes
information such as:

- crash date and year
- county and municipality
- crash severity
- fatalities and injuries
- crash type
- alcohol involvement
- drug involvement
- speeding
- distracted driving
- drowsy driving
- teen-driver involvement
- older-driver involvement
- unbelted crashes
- motorcycle involvement
- heavy-truck involvement
- pedestrian involvement
- bicycle involvement

# Raw Data

This directory is used for the original North Carolina statewide traffic
crash dataset analyzed in this project.

## Dataset Source

**Publisher:** North Carolina Department of Transportation (NCDOT)

**Dataset:** Statewide Crash Table

**Source URL:**  
https://ncdot.maps.arcgis.com/home/item.html?id=08ada689aca34927b0f78006fa885d36#overview

**Date accessed:** September 19, 2026

The dataset was downloaded from the NCDOT Statewide Crash Dashboard /
ArcGIS data source.

The exported dataset contains one record per reported crash and includes
information about crash location, severity, injuries, crash type, and
several crash-related characteristics.

## Data Snapshot Used in This Project

The downloaded dataset contains more than 1.7 million crash records
covering January 2021 through August 2026.

For reproducibility, this project treats the downloaded file as a
fixed snapshot of the NCDOT dataset. Because the NCDOT source may be
updated over time, users downloading the dataset at a later date may
observe slightly different record counts.

## Expected Local File

Download/export the dataset, extract the CSV if necessary, rename it to:

`nc_crashes.csv`

and place it at:

`data/raw/nc_crashes.csv`

The raw dataset is excluded from Git because of its size.

## Original Download

**Original downloaded archive:** `export-StatewideCrashTable.zip`

**File used for analysis after renaming csv file:** `nc_crashes.csv`