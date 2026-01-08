from dataclasses import dataclass
from typing import Tuple
import logging

from pyproj import Transformer
from pyproj.exceptions import ProjError
from rasterio.crs import CRS

from src.exceptions import CoordinateValidationError, CoordinateTransformationError
logger = logging.getLogger(__name__)

@dataclass
class CoordinateTransformer:
    
    #Coordinate transformation service
    # This component is responsible for transforming geographic coordinates
    # between:
    # - WGS84 (EPSG:4326), used by the API (latitude / longitude)
    # - The native CRS of the population dataset (e.g. ESRI:54009)
    # It guarantees:
    # - Consistent CRS handling (REQ5.12)
    # - Correct axis order (lon, lat) using always_xy=True
    

    dataset_crs: CRS
    _wgs84_to_dataset: Transformer = None
    _dataset_to_wgs84: Transformer = None

    def __post_init__(self):
        if not self.dataset_crs:
            raise ValueError("Dataset CRS must be defined")

        try: 
            # Transformer WGS84 -> Dataset CRS
            self._wgs84_to_dataset = Transformer.from_crs(
                "EPSG:4326",
                self.dataset_crs,
                always_xy=True  # enforces (lon, lat)
            )

            # Transformer Dataset CRS -> WGS84
            self._dataset_to_wgs84 = Transformer.from_crs(
                self.dataset_crs,
                "EPSG:4326",
                always_xy=True
            )
        except Exception as e:
            logger.error(f"Failed to initialize coordinate transformers: {e}")
            raise CoordinateTransformationError(
                f"Could not create coordinate transformer: {e}"
            ) from e

    def _validate_wgs84_coordinates(self, lat: float, lon: float) -> None:
        
        #Validate the WGS84 coordinates
        #Args:
        #    lat: Latitude in degrees
        #    lon: Longitude in degrees     
        #Raises:
        #    CoordinateValidationError: If coordinates are invalid
        
        # Check for None or null values
        if lat is None or lon is None:
            raise CoordinateValidationError("Latitude and longitude cannot be None")
        
        # Check type
        try:
            lat = float(lat)
            lon = float(lon)
        except (TypeError, ValueError) as e:
            raise CoordinateValidationError(
                f"Latitude and longitude must be numeric values: {e}"
            ) from e
        
        # Check ranges
        if not (-90.0 <= lat <= 90.0):
            raise CoordinateValidationError(
                f"Latitude must be between -90 and 90 degrees, got {lat}"
            )
        if not (-180.0 <= lon <= 180.0):
            raise CoordinateValidationError(
                f"Longitude must be between -180 and 180 degrees, got {lon}"
            )

    def to_dataset(self, lat: float, lon: float) -> Tuple[float, float]:
        
        # Transform coordinates from WGS84 to dataset CRS
        # Args:
        #     lat: latitude in degrees (-90 to 90)
        #     lon: longitude in degrees (-180 to 180)
        # Returns:
        #     Tuple of (x, y) in dataset CRS
        # Raises:
        #   CoordinateValidationError: If input coordinates are invalid
        #   CoordinateTransformationError: If transformation fails

        self._validate_wgs84_coordinates(lat, lon)

        try:
            x, y = self._wgs84_to_dataset.transform(lon, lat)

            if not (abs(x) < float('inf') and abs(y) < float('inf')):
                    raise CoordinateTransformationError(
                        f"Transformation resulted in invalid values: x={x}, y={y}"
                    )
            return x, y
    
        except ProjError as e:
            logger.error(f"Projection error during transformation: {e}")
            raise CoordinateTransformationError(
                f"Failed to transform coordinates ({lat}, {lon}): {e}"
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error during transformation: {e}")
            raise CoordinateTransformationError(
                f"Unexpected error transforming coordinates: {e}"
            ) from e

    def to_wgs84(self, x: float, y: float) -> Tuple[float, float]:
        
        # Transform coordinates from dataset CRS to WGS84
        # Input:
        #     (x, y) in dataset CRS
        # Output:
        #     Tuple of (lat, lon) in WGS84
        # Raises:
        #   CoordinateTransformationError: If transformation fails
        #    CoordinateValidationError: If input coordinates are invalid

        # Validate input
        if x is None or y is None:
            raise CoordinateValidationError("X and Y coordinates cannot be None")
        
        try:
            x = float(x)
            y = float(y)
        except (TypeError, ValueError) as e:
            raise CoordinateValidationError(
                f"X and Y must be numeric values: {e}"
            ) from e

        try:
            lon, lat = self._dataset_to_wgs84.transform(x, y)
            if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
                raise CoordinateTransformationError(
                    f"Transformation resulted in invalid WGS84 coordinates: "
                                        f"lat={lat}, lon={lon}"       
             )
            return lat, lon
    
        except ProjError as e:
            logger.error(f"Projection error during reverse transformation: {e}")
            raise CoordinateTransformationError(
                f"Failed to transform coordinates ({x}, {y}) to WGS84: {e}"
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error during reverse transformation: {e}")
            raise CoordinateTransformationError(
                f"Unexpected error transforming coordinates: {e}"
            ) from e
