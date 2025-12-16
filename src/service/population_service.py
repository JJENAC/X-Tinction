import rasterio
from rasterio.windows import Window
#from rasterio.warp import transform
import logging
from src.service.coordinate_transformer import CoordinateTransformer


logger = logging.getLogger(__name__)

class PopulationDensityService:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.dataset = None
        self.transformer = None

    def start(self):
        """Opens the raster dataset."""
        try:
            self.dataset = rasterio.open(self.data_path)
            self.transformer = CoordinateTransformer(self.dataset.crs)
        except Exception as e:
            logger.error(f"Failed to open dataset {self.data_path}: {e}")

    def stop(self):
        """Closes the raster dataset."""
        if self.dataset:
            self.dataset.close()

    def get_density(self, lat: float, lon: float) -> float:
        """
        Gets population density at the specified latitude and longitude.
        """
        if not self.dataset or not self.transformer:
            return -1.0

        try:
            # Transform coordinates 
            x, y = self.transformer.to_dataset(lat, lon)

            # Get pixel coordinates
            row, col = self.dataset.index(x, y)
            
            # Read single pixel
            window = Window(col, row, 1, 1)
            data = self.dataset.read(1, window=window)
            
            if data.size == 0:
                return 0.0
                
            val = data[0, 0]
            
            if val == self.dataset.nodata:
                return 0.0
                
            return float(val)
            
        except IndexError:
            # Coordinates out of bounds
            return 0.0
        except Exception as e:
            logger.error(f"Error querying density: {e}")
            return 0.0
