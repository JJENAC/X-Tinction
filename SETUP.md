# Dynamic UAV Data - Setup Guide

This guide provides step-by-step instructions to set up the Dynamic UAV Data project (First Version).

## 1. Prerequisites
- **Python 3.9+** installed on your system.
- **Git** (optional, for cloning).

## 2. Environment Setup
It is recommended to use a virtual environment to manage dependencies.

### Linux/macOS
```bash
# Navigate to the project directory
cd "First Version"

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### Windows
```powershell
# Navigate to the project directory
cd "First Version"

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

## 3. Install Dependencies
With the virtual environment activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

## 4. Download Data
The project requires global population data from the **Global Human Settlement Layer (GHSL)**.

1.  Go to the [GHSL Download Page](https://ghsl.jrc.ec.europa.eu/download.php?ds=pop).
2.  Look for the **GHS-POP R2023A** dataset.
3.  Select the **Global** coverage.
4.  Choose the **Mollweide (ESRI:54009)** projection.
5.  Choose the **100m** resolution.
6.  Look for the **R4_C19** tile (Toulouse region) or **Epoch 2030** file.
  - For Toulouse testing, use: `GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0_R4_C19.tif`
    - This is a regional tile that covers the Toulouse area, much smaller than the global dataset.
    - If you download a different tile, update the path in `src/main.py`.

7.  **Place the data**:
    - Create the directory `data/geographic_data/` if it doesn't exist.
    - Move your downloaded file (e.g., `GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0_R4_C19.tif`) into `data/geographic_data/`.

8.  **Configuration**:
    - By default, the application looks for: `data/geographic_data/GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0_R4_C19.tif`.
    - If your file has a different name, you can set the `DATA_PATH` environment variable when running, or rename the file.

## 5. Running the Application
Start the FastAPI server using `uvicorn`:

```bash
# Ensure you are in the 'First Version' directory
uvicorn src.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

## 6. Usage Example
You can query the population density API using `curl` or a web browser.

**Example Request:**
```bash
curl "http://127.0.0.1:8000/density?lat=43.6045&lon=1.444"
```

**Expected Response:**
```json
{
  "lat": 43.6045,
  "lon": 1.444,
  "density": 1234.56
}
```
*Note: The density returned is typically people per km² (check source code comments for specifics).*

**Check service health:**
Verify the service is running and dataset is loaded:
```bash
curl "http://127.0.0.1:8000/health"
```
**Expected Response:**
```json
{
  "status": "healthy",
  "service_initialized": true,
  "dataset_path": "data/geographic_data/GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0_R4_C19.tif",
  "dataset_crs": "ESRI:54009",
  "dataset_bounds": {
    "left": -18041000.0,
    "bottom": -9000000.0,
    "right": 18041000.0,
    "top": 9000000.0
  },
  "dataset_shape": {
    "height": 180000,
    "width": 360820
  }
}
```
**Invalid Request Examples:**
Invalid latitude (out of range):
```bash
curl "http://127.0.0.1:8000/density?lat=91&lon=0"
```
Missing parameters:
```bash
curl "http://127.0.0.1:8000/density"
```

**Running Tests:**
The project also includes a comprehensive test suite for error handling.

**Install Test Dependencies**
```bash
pip install pytest pytest-cov httpx
```
**Run All Tests:**
```bash
pytest tests/test_error_handling.py -v

pytest tests/test_error_handling.py --cov=src --cov-report=html
```
Expected Result: 19 tests passing (100% success rate)

**Error Handling**
The API includes error handling with clear error messages:

- **200 (Success):** Valid coordinates, returns population density
- **400 (Bad Request):** Invalid coordinates or coordinates outside dataset coverage
- **422 (Validation Error):** Missing parameters or wrong data type
- **503 (Service Unavailable):** Dataset not loaded or service initialization failed

**Troubleshooting**
**Service Returns 503 Error:**  
All requests return "Service not initialized"

-Check if the dataset file exists in `data/geographic_data/`
-Verify the file path matches the configuration
-Check server logs for startup errors
-Visit `/health` endpoint to see detailed status

**Tests Fail with Import Errors:**  
`ModuleNotFoundError` when running tests
```bash
pip install pytest httpx
```
**Invalid Coordinates Error:**  
Getting out of bounds errors for valid coordinates
- Visit `/health` endpoint to see dataset bounds
- Ensure coordinates are within dataset coverage area
- Check coordinates are in correct format (decimal degrees)

**Python Command Not Found:**
- On Windows, try `py` instead of `python`
- On Linux/macOS, try `python3` instead of `python`




