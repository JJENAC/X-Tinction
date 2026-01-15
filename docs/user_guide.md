# User Guide
# Dynamic Population Density Service
## 1. Purpose of the Service

The Dynamic Population Density Service provides an estimate of population density (people per km²) at a given geographic location.

It is designed to support:

- UAV mission planning
- U-space services
- Risk-aware operational decision-making

The service helps assess population exposure, which is a key parameter in aviation safety and risk analysis.

--------------------------------------------------------
## 2. Intended Users

This service is intended for:

- UAV operators
- U-space service providers
- System integrators
- Safety analysts
- Research and engineering teams

No programming knowledge is required to use the service.

--------------------------------------------------------
## 3. How to Use the Service

The service is accessed through a REST API.

Required Input:

- Latitude (decimal degrees)
- Longitude (decimal degrees)

Coordinates must be expressed in WGS84 (EPSG:4326) format.

--------------------------------------------------------
## 4. Example Usage
#### Requesting Population Density

Example request using a web browser or command line:

http://127.0.0.1:8000/density?lat=43.6045&lon=1.444

Example Response
{
  "lat": 43.6045,
  "lon": 1.444,
  "density": 9719.25
}

#### Interpretation of the Result

The returned value represents population density in people per km²

- A higher value indicates a higher population exposure
- A value of 0.0 corresponds to an unpopulated area

--------------------------------------------------------
## 5. Health Check

Users can verify service availability using the health endpoint:

http://127.0.0.1:8000/health


This endpoint confirms:

- Service availability
- Dataset loading status

---------------------------------------------------------
## 6. Typical Use Cases
#### UAV Mission Planning

- Assess population density along a planned flight path
- Identify high-risk urban areas
- Support flight authorization decisions

#### Risk Assessment

- Estimate ground risk exposure
- Safety assessments
- Input for decision-support tools

---------------------------------------------------------
## 7. Error Messages

The service returns explicit error messages when:

- Coordinates are invalid
- Required parameters are missing
- The dataset is unavailable

These messages help users quickly identify and correct input errors.

---------------------------------------------------------
## 8. Limitations

- Population data is static (single epoch)
- No temporal variation (day/night effects)
- Resolution limited to available dataset

Users should consider these limitations when interpreting results.

---------------------------------------------------------
## 9. Summary

The Dynamic Population Density Service provides a simple and reliable way to access population density information for geospatial decision-making.

It is designed to be:

- Easy to use
- Robust
- Transparent
- Suitable for operational and academic contexts

--------------------------------------------------------
## Authors:

Lou-Anne Gasp
Japjot Singh
Laxmi Pandey
Liana Chatterjee

ENAC – IATSED24 Master Program
In collaboration with Sopra Steria