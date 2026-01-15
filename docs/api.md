# API Documentation  
Dynamic Population Density Service

--------------------------------------------------------

## 1. Overview

The Dynamic Population Density Service exposes a REST API that provides population density estimates (people per km²) for a given geographic location expressed in latitude and longitude.

The API is designed to support UAV operations, U-space services, and risk-aware mission planning, where population exposure is a critical parameter for operational decision-making.

The service relies on geospatial raster data from the Global Human Settlement Layer (GHS-POP) and performs on-the-fly coordinate transformation and raster querying.

-------------------------------------------------------

## 2. API Specification

The API is implemented using **FastAPI** and formally specified using the **OpenAPI 3.1** standard.

An interactive API documentation interface (Swagger UI) is automatically generated and available when the service is running:

http://127.0.0.1:8000/docs

The raw OpenAPI specification is accessible at:

http://127.0.0.1:8000/openapi.json

------------------------------------------------------
## 3. Base URL

When running locally (Docker or local execution):

http://127.0.0.1:8000

------------------------------------------------------

## 4. Endpoints
### 4.1 Get Population Density

Retrieve the estimated population density at a given geographic location.

#### Endpoint
GET /density


#### Query Parameters

| Name | Type | Required | Description |
|-----|------|----------|-------------|
| lat | float | Yes | Latitude in decimal degrees(WGS84) |
| lon | float | Yes | Longitude in decimal degrees(WGS84) |

#### Example Request
bash
curl "http://127.0.0.1:8000/density?lat=43.6045&lon=1.444"

#### Response:
{
  "lat": 43.6045,
  "lon": 1.444,
  "density": 9719.25
}

#### Response Fields
Field	Type	    Description
lat	    float	    Input latitude
lon	    float	    Input longitude
density	float	    Population density in people per km²

-----------------------------------------------------------

### 4.2 Health Check
Verify service availability and dataset loading status.

#### Endpoint
GET /health

#### Example Request
curl "http://127.0.0.1:8000/health"

#### Example Response
{
  "status": "healthy",
  "service_initialized": true,
  "dataset_path": "data/geographic_data/GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0.tif"
}

-----------------------------------------------------------

## 5. Coordinate Reference Systems

Component	    CRS
API Input	    WGS84 (EPSG:4326)
Dataset	        Mollweide Projection (ESRI:54009)

All coordinate transformations are handled internally using PyProj, ensuring spatial accuracy and correct axis ordering.

-----------------------------------------------------------
## 6. Error Handling
The API provides explicit and meaningful HTTP status codes.

HTTPCode    Meaning	         Description
200	         OK              Valid request, density successfully returned
400	     Bad Request	     Invalid or out-of-range coordinates
422	   Unprocessable Entity  Missing or malformed query parameters
503	   Service Unavailable	 Dataset not loaded or service initialization failure

#### Example Error Response
{
  "detail": "Latitude must be between -90 and 90 degrees"
}

-----------------------------------------------------------
## 7. Validation and Robustness

- Input parameters are validated automatically using FastAPI and Pydantic 
- Coordinates outside dataset coverage are explicitly rejected
- All exceptions are handled using custom exception classes to ensure consistent API responses

-----------------------------------------------------------
## 8. Testing

The API behavior, robustness and performance are validated using an automated test suite based on **pytest**.

The test strategy combines unit tests, integration tests and performance checks to ensure functional correctness and operational reliability.

### Test Coverage

The test suite includes:

- **Unit tests**
  - Coordinate validation (latitude/longitude ranges)
  - Coordinate transformation errors (CRS, projection failures)
  - Dataset loading and initialization errors

- **Integration tests**
  - End-to-end API requests using FastAPI TestClient
  - Validation of HTTP status codes and response payloads
  - Error response structure consistency

- **Performance tests**
  - API response time (< 500 ms)
  - Service startup time (< 15 minutes)

- **Boundary and edge cases**
  - Geographic boundary values (±90°, ±180°)
  - Out-of-bounds coordinates
  - Unpopulated areas (zero density)

Each test case is traceable to functional and user requirements (TC20–TC32, URx, Rx).

### Running the Tests
pytest

-----------------------------------------------------------
## 9. Limitations

- Static population dataset (single epoch)
- No temporal population variation
- Performance limited by raster access (no caching)
- Coverage limited to available GHS-POP data

-----------------------------------------------------------
## 10. Future Improvements

- Support for multiple datasets and epochs
- Time-dependent population density modeling
- Request caching and performance optimization
- Authentication and access control
- Deployment on cloud platforms
