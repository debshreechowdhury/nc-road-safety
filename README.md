# Beyond the Crash Count

## Understanding Crash Severity Across North Carolina

This project analyzes statewide traffic crash records published by the
North Carolina Department of Transportation (NCDOT).

Rather than looking only at how many crashes occur, the project explores
an additional question:

> Where do crashes happen most often, and where or under what
> circumstances are recorded crashes more likely to result in fatal or
> serious injury?

The project is designed to communicate road-safety patterns to a general audience
while maintaining a reproducible analysis workflow.

---

## Project Questions

The analysis is organized around three main questions:

1. How has the volume and severity of reported crashes changed across
   North Carolina from 2021 through 2025?

2. Does the geographic pattern of crash frequency differ from the
   geographic pattern of serious crash outcomes?

3. Which recorded crash characteristics are common, and which are
   associated with disproportionately serious outcomes?

---

## Analysis Period

The downloaded NCDOT dataset contains records from 2021 through part of
2026.

The project's primary analysis uses:

```text
2021–2025

## Dataset

This project uses the **NCDOT Statewide Crash Table**, published by the
North Carolina Department of Transportation.

**Data source:** https://ncdot.maps.arcgis.com/home/item.html?id=08ada689aca34927b0f78006fa885d36#overview

The downloaded data contain statewide reported crash records from 2021
through August 2026. The primary analysis uses the five complete calendar
years **2021–2025**.

For detailed download instructions, data provenance, and local file setup,
see [`data/raw/README.md`](data/raw/README.md).