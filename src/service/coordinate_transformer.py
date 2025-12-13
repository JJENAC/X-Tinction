from dataclasses import dataclass
from typing import Tuple

from pyproj import Transformer
from rasterio.crs import CRS


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

    def to_dataset(self, lat: float, lon: float) -> Tuple[float, float]:
        
        # Transform coordinates from WGS84 to dataset CRS
        # Input:
        #     lat: latitude in degrees (-90 to 90)
        #     lon: longitude in degrees (-180 to 180)
        # Output:
        #     (x, y) in dataset CRS
        
        if not (-90.0 <= lat <= 90.0):
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not (-180.0 <= lon <= 180.0):
            raise ValueError("Longitude must be between -180 and 180 degrees")

        x, y = self._wgs84_to_dataset.transform(lon, lat)
        return x, y

    def to_wgs84(self, x: float, y: float) -> Tuple[float, float]:
        
        # Transform coordinates from dataset CRS to WGS84
        # Input:
        #     (x, y) in dataset CRS
        # Output:
        #     (lat, lon) in WGS84
        
        lon, lat = self._dataset_to_wgs84.transform(x, y)
        return lat, lon
