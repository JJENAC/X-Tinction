import rasterio
from rasterio.windows import Window
from rasterio.errors import RasterioIOError
#from rasterio.warp import transform
import logging
from typing import Optional

from src.service.coordinate_transformer import CoordinateTransformer
from src.exceptions import (
    DatasetError,
    OutOfBoundsError,
    CoordinateValidationError,
    CoordinateTransformationError
)

logger = logging.getLogger(__name__)

class PopulationDensityService:
    def __init__(self, data_path: str):
        if not data_path:
            raise ValueError("data_path cannot be empty")
        self.data_path = data_path
        self.dataset: Optional[rasterio.DatasetReader] = None
        self.transformer: Optional[CoordinateTransformer]= None

    def start(self):
        """Opens the raster dataset."""
        # Raises:
        #    DatasetError: If the dataset cannot be opened
        try:
            self.dataset = rasterio.open(self.data_path)
            logger.info(f"Successfully opened dataset: {self.data_path}")
            logger.info(f"Dataset CRS: {self.dataset.crs}")
            logger.info(f"Dataset bounds: {self.dataset.bounds}")
            logger.info(f"Dataset shape: {self.dataset.shape}")
            self.transformer = CoordinateTransformer(self.dataset.crs)
        except FileNotFoundError as e:
            logger.error(f"Dataset file not found: {self.data_path}")
            raise DatasetError(
                f"Dataset file not found: {self.data_path}"
            ) from e
        except RasterioIOError as e:
            logger.error(f"Failed to read dataset {self.data_path}: {e}")
            raise DatasetError(
                f"Failed to read raster dataset: {e}"
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error opening dataset {self.data_path}: {e}")
            raise DatasetError(
                f"Failed to open dataset: {e}"
            ) from e

    def stop(self):
        """Closes the raster dataset."""
        if self.dataset:
            try:
                self.dataset.close()
                logger.info("Dataset closed successfully")
            except Exception as e:
                logger.warning(f"Error closing dataset: {e}")

    def _is_within_bounds(self, x: float, y: float) -> bool:
        #Check if coordinates are within dataset bounds
        if not self.dataset:
            return False
        
        bounds = self.dataset.bounds
        return (bounds.left <= x <= bounds.right and 
                bounds.bottom <= y <= bounds.top)            

    def get_density(self, lat: float, lon: float) -> float:
        """
        Gets population density at the specified latitude and longitude.
        Args:
            lat: Latitude in WGS84 (degrees)
            lon: Longitude in WGS84 (degrees)
            
        Returns:
            Population density per 100m² (multiply by 100 for density per km²)
            Returns 0.0 for no-data areas within bounds
            
        Raises:
            DatasetError: If dataset is not initialized
            CoordinateValidationError: If coordinates are invalid
            CoordinateTransformationError: If coordinate transformation fails
            OutOfBoundsError: If coordinates are outside dataset coverage
        """
        # Check if service is initialized
        if not self.dataset or not self.transformer:
            logger.error("Service not properly initialized")
            raise DatasetError(
                "Service not initialized. Call start() first."
            )

        try:
            # Transform coordinates 
            x, y = self.transformer.to_dataset(lat, lon)
            logger.debug(f"Transformed ({lat}, {lon}) to ({x}, {y})")
        
        except (CoordinateValidationError, CoordinateTransformationError) as e:
            # Re-raise the coordinate errors as-is
            logger.warning(f"Coordinate error for ({lat}, {lon}): {e}")
            raise

        if not self._is_within_bounds(x, y):
            logger.warning(
                f"Coordinates ({lat}, {lon}) -> ({x}, {y}) "
                f"are outside dataset bounds {self.dataset.bounds}"
            )
            raise OutOfBoundsError(
                f"Coordinates ({lat}, {lon}) are outside the dataset coverage area"
            )
        
        try:
            # Gets the pixel coordinates
            row, col = self.dataset.index(x, y)
            logger.debug(f"Pixel coordinates: row={row}, col={col}")
            
            # Validate pixel coordinates
            if row < 0 or row >= self.dataset.height or col < 0 or col >= self.dataset.width:
                raise OutOfBoundsError(
                    f"Pixel coordinates ({row}, {col}) are outside raster dimensions "
                    f"({self.dataset.height}, {self.dataset.width})"
                )
            
            # Reads a single pixel
            window = Window(col, row, 1, 1)
            data = self.dataset.read(1, window=window)
            
            # Check if data was read
            if data.size == 0:
                logger.warning(f"No data read for pixel ({row}, {col})")
                return 0.0
            
            val = data[0, 0]

            if self.dataset.nodata is not None and val == self.dataset.nodata:
                logger.debug(f"No-data value at ({lat}, {lon})")
                return 0.0
            
            density = float(val)
            if density < 0:
                logger.warning(
                    f"Negative density value {density} at ({lat}, {lon}), returning 0.0"
                )
                return 0.0
            
            logger.debug(f"Density at ({lat}, {lon}): {density}")
            return density
        
        except OutOfBoundsError:
            # Re-raise the out of bounds errors
            raise
        except (ValueError, TypeError) as e:
            logger.error(f"Data type error reading density: {e}")
            raise DatasetError(
                f"Invalid data type in raster at coordinates ({lat}, {lon}): {e}"
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error querying density at ({lat}, {lon}): {e}")
            raise DatasetError(
                f"Error reading density data: {e}"
            ) from e
