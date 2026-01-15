### PROJECT : Dynamic Population Density Service

The Dynamic Population Density Service is a containerized REST API that provides population density estimates (people per km²) for a given geographic location expressed in latitude and longitude.

The service is designed to support UAV operations, U-space services, and risk-aware mission planning, where population exposure is a key decision parameter.

It relies on open geospatial data from the Global Human Settlement Layer (GHS-POP) and exposes a simple, robust HTTP interface.

This project was developed as part of the ENAC – IATSED Master Program, in collaboration with Sopra Steria.

------------------------------------------------------

## Key Features: 

- REST API built with FastAPI
- Population density extraction from GHS-POP raster datasets
- Accurate coordinate transformation (WGS84 → dataset CRS)
- Robust input validation and error handling
- Fully Dockerized for reproducible deployment
- Interactive API documentation via Swagger UI

------------------------------------------------------
## Architecture overview: 

Client
  ↓
FastAPI REST API
  ↓
Coordinate Transformation (WGS84 → Dataset CRS)
  ↓
Raster Dataset (GHS-POP)
  ↓
Population Density Computation
  ↓
JSON Response

------------------------------------------------------

## Technologies used : 

- Python 3 (Main programming language used to implement the API logic, data processing and geospatial computations)

- FastAPI (Framework to build the REST API, chosen for high performance, automatic request validation and built-in interactive documentation)

- Rasterio (Library used to read and query geospatial raster datasets such as GHS-POP population grids)

- PyProj (Used to accurately transform geographic coordinates between WGS84 (latitude/longitude) and the dataset’s native coordinate reference system)

- Docker (Used to containerize the application, ensuring reproducible deployment and simplified installation on any platform)

- Pytest (Testing framework used to validate API behavior, error handling, and service robustness)

------------------------------------------------------
------------------------------------------------------

### Getting Started (Docker Recommended)

## Prerequisites:

- Docker (Docker Desktop or Docker Engine)

------------------------------------------------------
# Build the Docker Image
From the project root directory:

docker build -t population-density-api

------------------------------------------------------
# Run the Container:

docker run --rm -p 8000:8000 \
  -v "$(pwd)/data:/app/data" \
  population-density-api

The API will be available at:

http://127.0.0.1:8000

------------------------------------------------------
------------------------------------------------------
### API Documentation

Interactive API (Swagger)
FastAPI automatically exposes an interactive documentation interface:

http://127.0.0.1:8000/docs

------------------------------------------------------
------------------------------------------------------

### API Usage

Endpoint: Get Population Density

## Request :
GET /density?lat={latitude}&lon={longitude}

Example:
curl "http://127.0.0.1:8000/density?lat=43.6045&lon=1.444"


## Response:

{
  "lat": 43.6045,
  "lon": 1.444,
  "density": 9719.25
}

## Returned value:
Population density expressed in people per km².

-----------------------------------------------------
-----------------------------------------------------

### Dataset

The service uses population data from the Global Human Settlement Layer (GHS-POP), provided by the European Commission Joint Research Centre (JRC).

Due to its size, the dataset is not included in the repository.

Expected Dataset Location:

data/geographic_data/
└── GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0.tif

Detailed setup instructions are available in SETUP.md.

----------------------------------------------------
----------------------------------------------------
### Coordinate Reference Systems

- API input: WGS84 (EPSG:4326 – latitude / longitude)
- Dataset CRS: Mollweide projection (ESRI:54009)

All coordinate transformations are handled internally using PyProj, ensuring correct axis order and spatial accuracy.

----------------------------------------------------
### Error Handling:

The API provides explicit HTTP error codes:

- 200 OK = Valid request, population density returned
- 400 Bad Request = Invalid or out-of-range coordinates
- 422 Unprocessable Entity = Missing or invalid query parameters
- 503 Service Unavailable = Dataset not loaded or service initialization failure

----------------------------------------------------
### Testing

A test suite is provided to validate API behavior and error handling.

Run tests locally:
pytest

Generate coverage report:
pytest --cov=src --cov-report=html


----------------------------------------------------
----------------------------------------------------
### Limitations :

- Static population dataset (single epoch)
- No temporal population variation
- No caching or performance optimization
- Coverage limited to available dataset tiles

### Future Improvements:
- Support for multiple population datasets
- Time-dependent population modeling
- Caching and performance optimization
- CI/CD integration
- Cloud-native deployment

------------------------------------------------------
### Authors:

Lou-Anne Gasp
Japjot Singh
Laxmi Pandey
Liana Chatterjee

ENAC – IATSED24 Master Program
In collaboration with Sopra Steria