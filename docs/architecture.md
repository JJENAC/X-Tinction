# Architecture Documentation
# Dynamic Population Density Service

## 1. Purpose of This Document

This document describes the software architecture of the Dynamic Population Density Service.
### It explains:

- The global system structure
- The main architectural components
- Data flows and responsibilities
- Design decisions and rationale

### This document is intended for:
- Technical stakeholders
- System engineers
- Developers integrating or extending the service

-------------------------------------------------------------------

## 2. Architectural Overview

The Dynamic Population Density Service is designed as a stateless, containerized REST service exposing population density information through a well-defined API.

The architecture follows a layered design, separating:

- API interface
- Business logic
- Geospatial processing
- Data access

This separation improves maintainability, testability, and extensibility.

-------------------------------------------------------------------
## 3. High-Level Architecture
### 3.1 Logical Architecture

Client (UAV / U-space / External System)
              |
              v
        FastAPI REST Layer
              |
              v
     Population Density Service
              |
              v
     Coordinate Transformation
              |
              v
       Raster Dataset (GHS-POP)

### 3.2 Responsibilities by Layer
Layer	                 Responsibility
Client	                 Sends HTTP requests with geographic coordinates
REST API (FastAPI)	     Request validation, routing, response formatting
Service Layer	         Business logic and population density computation
Transformation Layer	 CRS transformation (WGS84 → dataset CRS)
Data Layer	             Raster access and pixel value extraction

------------------------------------------------------------------
## 4. Component Architecture
### 4.1 API Layer

Technology: FastAPI

#### Main responsibilities:

- Expose REST endpoints (/density, /health)
- Validate input parameters
- Map exceptions to HTTP status codes
- Provide OpenAPI / Swagger documentation

#### Key file:
main.py

### 4.2 Service Layer

Component: PopulationDensityService

#### Responsibilities:

- Dataset loading and lifecycle management
- Density computation logic
- Bounds checking
- Error handling related to dataset access

#### Key file:
src/service/population_service.py

### 4.3 Coordinate Transformation Layer

Component: CoordinateTransformer

#### Responsibilities:

- Validate latitude and longitude ranges
- Convert coordinates from WGS84 (EPSG:4326)
- Transform to dataset CRS (ESRI:54009)

Technology: PyProj

#### Key file:
src/service/coordinate_transformer.py

## 4.4 Data Access Layer

#### Dataset:
Global Human Settlement Layer – Population (GHS-POP)

#### Characteristics:

- Raster-based population grid
- Mollweide projection (ESRI:54009)
- Static dataset (single epoch)

#### Access method:
Rasterio window-based reading

### 4.5 Exception Handling

- Custom exception classes ensure:
- Clear error semantics
- Consistent API responses
- Separation between technical and functional errors

Examples:
- CoordinateValidationError
- CoordinateTransformationError
- DatasetError
- OutOfBoundsError

#### Key file:
src/exceptions.py

----------------------------------------------------------------
## 5. Data Flow Description
### 5.1 Density Request Flow

- Client sends GET /density?lat=...&lon=...
- FastAPI validates query parameters
- CoordinateTransformer converts coordinates
- PopulationDensityService checks dataset bounds
- Raster pixel value is extracted
- Density is computed and normalized
- JSON response is returned to the client

----------------------------------------------------------------
## 6. Deployment Architecture
### 6.1 Containerization

The service is fully containerized using Docker.

#### Benefits:
- Reproducible deployment
- Environment consistency
- Simplified installation for clients
- Container contents:
- Python runtime
- System dependencies (GDAL, PROJ)
- Application source code

### 6.2 Runtime Configuration

- Dataset path configurable via environment variable
- Stateless execution model
- No persistent storage inside the container

--------------------------------------------------------------
## 7. Testing Architecture

#### Testing follows a multi-level strategy:

- Level	Scope
- Unit Tests	Individual components (transformer, validation)
- Integration Tests	Full API request lifecycle
- Performance Tests	Response time and startup time

Tests are implemented using pytest and FastAPI TestClient.

---------------------------------------------------------------

## 8. Design Decisions and Rationale
Decision:	                    Rationale:
FastAPI	                        High performance, automatic validation, OpenAPI support
Raster-based approach	        Accurate population modeling
Stateless service	            Scalability and simplicity
Docker deployment	            Platform independence
Layered architecture	        Maintainability and testability

-----------------------------------------------------------------
## 9. Limitations

- Single population dataset
- No temporal dimension
- No caching mechanism
- Local file-based dataset access

----------------------------------------------------------------
## 10. Future Architectural Evolutions

- Support for multiple datasets and projections
- Dataset abstraction layer
- Caching and spatial indexing
- Cloud-native deployment (Kubernetes)
- Integration into UAV mission planning pipelines

----------------------------------------------------------------
## 11. Summary

The Dynamic Population Density Service architecture emphasizes:

- Clarity
- Robustness
- Reproducibility
- Engineering best practices

It provides a solid foundation for operational UAV risk assessment and future system extensions.

----------------------------------------------------------------
## Authors:

Lou-Anne Gasp
Japjot Singh
Laxmi Pandey
Liana Chatterjee

ENAC – IATSED24 Master Program
In collaboration with Sopra Steria