# Dataset Documentation
# Dynamic Population Density Service
## 1. Purpose of This Document

This document describes the population dataset used by the Dynamic Population Density Service.
It explains:

- The dataset origin and provider
- Spatial characteristics and resolution
- Coordinate reference system
- Data semantics and limitations
- How the dataset is integrated into the service
- This document is intended for:
- Technical stakeholders
- System engineers
- Data analysts
- UAV / U-space domain experts

------------------------------------------------------------
## 2. Dataset Overview

The service relies on population data from the Global Human Settlement Layer – Population (GHS-POP).
GHS-POP is an open global dataset produced by the European Commission – Joint Research Centre (JRC).
It provides gridded population counts derived from census data and spatial modeling techniques.

#### Dataset Role in the System
The dataset is used to:

- Estimate population exposure at a given geographic location
- Support risk-aware UAV mission planning
- Enable population-based decision-making in U-space services

-------------------------------------------------------------

## 3. Dataset Identification
Attribute	Value
Dataset Name	GHS-POP
Release	R2023A
Epoch	2030
Coverage	Global
Spatial Resolution	100 m
Projection	Mollweide
CRS	ESRI:54009
Data Type	Raster (GeoTIFF)
Provider	European Commission – JRC
File Used by the Service
GHS_POP_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C19.tif (Toulouse region)

-------------------------------------------------------------
## 4. Spatial Characteristics
### 4.1 Coordinate Reference System (CRS)

Component:	           CRS:
API Input	           WGS84 (EPSG:4326)
Dataset	               Mollweide Projection (ESRI:54009)

The Mollweide projection is an equal-area projection, making it suitable for population density analysis. All coordinate transformations are handled internally using PyProj, ensuring spatial accuracy and correct axis ordering.

### 4.2 Spatial Resolution

- Pixel size: 100 m × 100 m
- Each raster cell represents population count within its area
- Population density is computed and normalized to people per km²
- This resolution provides a good trade-off between:
- Global coverage
- Computational efficiency
- Urban-scale accuracy

-----------------------------------------------------------
## 5. Data Semantics
### 5.1 Pixel Values

Each raster pixel contains an estimated population count. Values are derived from census data and spatial modeling. Non-populated areas (oceans, deserts, polar regions) typically contain zero or no-data values

### 5.2 NoData Handling

Pixels with no-data values are treated as zero population

This ensures robust behavior for:

- Uninhabited regions
- Boundary cases
- Polar areas

--------------------------------------------------------------
## 6. Dataset Integration in the Service
### 6.1 Loading Strategy

- The dataset is loaded once at service startup
- Dataset loading is validated via the /health endpoint
- Dataset path is configurable via environment variable

### 6.2 Query Mechanism

For each API request:

- Input coordinates (lat, lon) are validated
- Coordinates are transformed to dataset CRS
- Dataset bounds are checked
- The corresponding raster cell is read
- Population density is computed and returned

This approach ensures:
- Deterministic behavior
- Low memory overhead
- Accurate spatial querying

-----------------------------------------------------------
## 7. Dataset Size and Distribution

Due to its size, the dataset is not included in the Git repository.

#### Expected Directory Structure
data/geographic_data/
└── GHS_POP_E2020_GLOBE_R2023A_54009_100_V1_0_R4_C19.tif

#### Dataset Download

The dataset can be obtained from the official GHS website:

https://ghsl.jrc.ec.europa.eu/download.php?ds=pop

Detailed setup instructions are provided in SETUP.md.

-----------------------------------------------------------
## 8. Limitations

- Static dataset (single temporal snapshot – epoch 2030)
- No real-time or seasonal population variation
- Resolution limited to 100 m
- Accuracy depends on census data quality and modeling assumptions

These limitations are inherent to global population datasets and are explicitly documented to ensure transparency.

------------------------------------------------------------
## 9. Future Dataset Extensions
#### Potential future improvements include:

- Support for multiple epochs (temporal analysis)
- Integration of alternative population datasets
- Higher-resolution regional datasets
- Dynamic population modeling (day/night population)

------------------------------------------------------------
## 10. Summary

The GHS-POP dataset provides a reliable and well-documented foundation for population-based risk assessment. Its integration into the Dynamic Population Density Service enables:

- Accurate population exposure estimation
- Reproducible geospatial analysis
- Scalable deployment in UAV and U-space contexts

---------------------------------------------------------
## References

European Commission – Joint Research Centre
https://ghsl.jrc.ec.europa.eu/

GHS-POP R2023A Documentation
https://ghsl.jrc.ec.europa.eu/download.php

----------------------------------------------------------
## Authors:

Lou-Anne Gasp
Japjot Singh
Laxmi Pandey
Liana Chatterjee

ENAC – IATSED24 Master Program
In collaboration with Sopra Steria