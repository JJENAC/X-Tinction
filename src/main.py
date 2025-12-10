import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from src.service.population_service import PopulationDensityService

# Default path to the VRT or TIF file
DATA_PATH = os.getenv("DATA_PATH", "data/geographic_data/GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0.vrt")

service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global service
    service = PopulationDensityService(DATA_PATH)
    service.start()
    yield
    service.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/density")
async def get_density(lat: float, lon: float):
    if not service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    density = service.get_density(lat, lon)
    
    # Note: The original requirement might have been to return people/km2.
    # GHSL 100m gives people per cell (100x100m = 0.01 km2).
    # So density per km2 = value * 100.
    # Assuming the service returns the raw value, we might convert it here or return as is.
    # Based on previous summary, it "converts raw count to people/km²".
    
    density_per_km2 = density * 100
    
    return {
        "lat": lat,
        "lon": lon,
        "density": density_per_km2
    }
