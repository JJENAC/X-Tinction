from src.service.population_service import PopulationDensityService

# Path to a sample TIF file (adjust as needed for local environment)
path = "data/geographic_data/GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0_R4_C19.tif"

print(f"Initializing service with {path}...")
service = PopulationDensityService(path)
service.start()

# Test coordinates (Approx Toulouse center)
lat, lon = 43.6045, 1.444

print(f"Querying {lat}, {lon}...")
density = service.get_density(lat, lon)

print(f"Service Result: {density}")
service.stop()
