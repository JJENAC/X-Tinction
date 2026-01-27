import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

from src.service.population_service import PopulationDensityService
from src.exceptions import (
    CoordinateValidationError,
    CoordinateTransformationError,
    DatasetError,
    OutOfBoundsError,
    PopulationDensityError
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default path to the TIF file inside data folder
# Using global dataset to query any location worldwide
DATA_PATH = os.getenv(
    "DATA_PATH",
    "data/geographic_data/GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0.tif"
)


service = None

class DensityResponse(BaseModel):
    """Response model for density queries."""
    lat: float = Field(..., description="Latitude in WGS84")
    lon: float = Field(..., description="Longitude in WGS84")
    density: float = Field(..., description="Population density per km²")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: str = Field(None, description="Additional error details")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global service
    try:
        logger.info(f"Starting service with data path: {DATA_PATH}")
        service = PopulationDensityService(DATA_PATH)
        service.start()
        logger.info("Service started successfully")
        yield
    except DatasetError as e:
        logger.critical(f"Failed to start service: {e}")
        # here service will be none and endpoint will return 503
        yield
    except Exception as e:
        logger.critical(f"Unexpected error during startup: {e}")
        yield
    finally:
        if service:
            logger.info("Shutting down service")
        service.stop()

app = FastAPI(
    title="Population Density API",
    description="API for querying global population density data",
    version="1.0.0",
    lifespan=lifespan)

@app.exception_handler(PopulationDensityError)
async def population_density_error_handler(request, exc: PopulationDensityError):
    #Handle custom population density errors
    logger.error(f"Population density error: {exc}")
    
    # Map exceptions to HTTP status codes
    status_code = 500
    error_type = "internal_error"
    
    if isinstance(exc, CoordinateValidationError):
        status_code = 400
        error_type = "invalid_coordinates"
    elif isinstance(exc, OutOfBoundsError):
        status_code = 400
        error_type = "out_of_bounds"
    elif isinstance(exc, CoordinateTransformationError):
        status_code = 400
        error_type = "transformation_error"
    elif isinstance(exc, DatasetError):
        status_code = 503
        error_type = "dataset_error"
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_type,
            "message": str(exc),
            "detail": type(exc).__name__
        }
    )

@app.get(
        "/density",
        response_model=DensityResponse,
    responses={
        200: {"description": "Successful response with density data"},
        400: {
            "model": ErrorResponse,
            "description": "Invalid input parameters"
        },
        503: {
            "model": ErrorResponse,
            "description": "Service unavailable"
        }
    }
)

async def get_density(
    lat: float = Query(
        ...,
        description="Latitude in WGS84 (degrees)",
        ge=-90.0,
        le=90.0,
        examples =[48.8566]
    ),
    lon: float = Query(
        ...,
        description="Longitude in WGS84 (degrees)",
        ge=-180.0,
        le=180.0,
        examples = [2.3522]
    )
    ):
    """
    Get population density at specified coordinates.
    
    Returns population density per km² at the given latitude and longitude.
    Uses global population data in ESRI:54009 projection.
    
    Parameters:
    - **lat**: Latitude in degrees (-90 to 90)
    - **lon**: Longitude in degrees (-180 to 180)
    
    Returns:
    - Population density per km²
    - Returns 0 for areas with no population data
    
    Raises:
    - 400: Invalid coordinates or coordinates outside dataset coverage
    - 503: Service not available (dataset not loaded)
    """
    if not service:
        logger.error("Service not initialized")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "service_unavailable",
                "message": "Service is not initialized. Dataset may have failed to load.",
                "detail": "Check server logs for more information"
            }
        )
    
    try:
        # Get density (this handles all validation and transformation)
        density_per_100m2 = service.get_density(lat, lon)
        
        # Convert to density per km² (100m × 100m = 10,000 m² = 0.01 km²)
        # So multiply by 100 to get density per km²
        density_per_km2 = density_per_100m2 * 100
        
        logger.info(
            f"Successfully retrieved density for ({lat}, {lon}): "
            f"{density_per_km2:.2f} per km²"
        )
        
        return DensityResponse(
            lat=lat,
            lon=lon,
            density=density_per_km2
        )
        
    except (CoordinateValidationError, 
            CoordinateTransformationError, 
            OutOfBoundsError,
            DatasetError) as e:
        raise
    except Exception as e:
        # Catch-all for unexpected errors
        logger.error(f"Unexpected error in get_density endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred",
                "detail": str(e)
            }
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns service status and dataset information.
    """
    if not service or not service.dataset:
        return {
            "status": "unhealthy",
            "service_initialized": False,
            "message": "Service or dataset not initialized"
        }
    
    try:
        return {
            "status": "healthy",
            "service_initialized": True,
            "dataset_path": service.data_path,
            "dataset_crs": str(service.dataset.crs),
            "dataset_bounds": {
                "left": service.dataset.bounds.left,
                "bottom": service.dataset.bounds.bottom,
                "right": service.dataset.bounds.right,
                "top": service.dataset.bounds.top
            },
            "dataset_shape": {
                "height": service.dataset.height,
                "width": service.dataset.width
            }
        }
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return {
            "status": "unhealthy",
            "service_initialized": True,
            "error": str(e)
        }

    
    
