import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock

from src.exceptions import (
    CoordinateValidationError,
    CoordinateTransformationError,
    DatasetError,
    OutOfBoundsError
)


class TestCoordinateValidation:
    """Test coordinate validation errors."""
    
    def test_latitude_too_high(self):
        """Test latitude > 90."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        
        with pytest.raises(CoordinateValidationError) as exc:
            transformer.to_dataset(91.0, 0.0)
        assert "Latitude must be between -90 and 90" in str(exc.value)
    
    def test_latitude_too_low(self):
        """Test latitude < -90."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        
        with pytest.raises(CoordinateValidationError) as exc:
            transformer.to_dataset(-91.0, 0.0)
        assert "Latitude must be between -90 and 90" in str(exc.value)
    
    def test_longitude_too_high(self):
        """Test longitude > 180."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        
        with pytest.raises(CoordinateValidationError) as exc:
            transformer.to_dataset(0.0, 181.0)
        assert "Longitude must be between -180 and 180" in str(exc.value)
    
    def test_longitude_too_low(self):
        """Test longitude < -180."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        
        with pytest.raises(CoordinateValidationError) as exc:
            transformer.to_dataset(0.0, -181.0)
        assert "Longitude must be between -180 and 180" in str(exc.value)
    
    def test_null_latitude(self):
        """Test None latitude."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        
        with pytest.raises(CoordinateValidationError) as exc:
            transformer.to_dataset(None, 0.0)
        assert "cannot be None" in str(exc.value)
    
    def test_null_longitude(self):
        """Test None longitude."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        
        with pytest.raises(CoordinateValidationError) as exc:
            transformer.to_dataset(0.0, None)
        assert "cannot be None" in str(exc.value)
    
    def test_non_numeric_latitude(self):
        """Test non-numeric latitude."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        
        with pytest.raises(CoordinateValidationError) as exc:
            transformer.to_dataset("invalid", 0.0)
        assert "must be numeric" in str(exc.value)
    
    def test_non_numeric_longitude(self):
        """Test non-numeric longitude."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        
        with pytest.raises(CoordinateValidationError) as exc:
            transformer.to_dataset(0.0, "invalid")
        assert "must be numeric" in str(exc.value)


class TestCoordinateTransformation:
    """Test coordinate transformation errors."""
    
    @patch('pyproj.Transformer.transform')
    def test_transformation_returns_infinity(self, mock_transform):
        """Test transformation resulting in infinity."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        mock_transform.return_value = (float('inf'), 0.0)
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        
        with pytest.raises(CoordinateTransformationError) as exc:
            transformer.to_dataset(45.0, 90.0)
        assert "invalid values" in str(exc.value)
    
    @patch('pyproj.Transformer.transform')
    def test_transformation_throws_proj_error(self, mock_transform):
        """Test pyproj throwing an error."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        from pyproj.exceptions import ProjError
        
        mock_transform.side_effect = ProjError("Projection failed")
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        
        with pytest.raises(CoordinateTransformationError) as exc:
            transformer.to_dataset(45.0, 90.0)
        assert "Failed to transform" in str(exc.value)


class TestDatasetErrors:
    """Test dataset-related errors."""
    
    def test_dataset_file_not_found(self):
        """Test missing dataset file."""
        from src.service.population_service import PopulationDensityService
        
        service = PopulationDensityService("nonexistent_file.tif")
        
        with pytest.raises(DatasetError) as exc:
            service.start()
        assert "no such file" in str(exc.value).lower()
    
    def test_service_not_initialized(self):
        """Test querying density before initialization."""
        from src.service.population_service import PopulationDensityService
        
        service = PopulationDensityService("dummy.tif")
        
        with pytest.raises(DatasetError) as exc:
            service.get_density(48.8566, 2.3522)
        assert "not initialized" in str(exc.value).lower()


class TestOutOfBounds:
    """Test out-of-bounds coordinate errors."""
    
    @patch('src.service.population_service.PopulationDensityService._is_within_bounds')
    def test_coordinates_outside_bounds(self, mock_bounds):
        """Test coordinates outside dataset bounds."""
        from src.service.population_service import PopulationDensityService
        from rasterio.crs import CRS
        
        # Mock the service
        service = PopulationDensityService("dummy.tif")
        service.dataset = MagicMock()
        service.dataset.crs = CRS.from_string("ESRI:54009")
        service.transformer = Mock()
        service.transformer.to_dataset = Mock(return_value=(1000000, 1000000))
        
        # Mock bounds check to return False
        mock_bounds.return_value = False
        
        with pytest.raises(OutOfBoundsError) as exc:
            service.get_density(89.0, 179.0)
        assert "outside" in str(exc.value).lower()


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_exact_boundary_latitude_90(self):
        """Test latitude = 90 (North Pole)."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        # Should not raise an error
        x, y = transformer.to_dataset(90.0, 0.0)
        assert x is not None and y is not None
    
    def test_exact_boundary_latitude_minus_90(self):
        """Test latitude = -90 (South Pole)."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        # Should not raise an error
        x, y = transformer.to_dataset(-90.0, 0.0)
        assert x is not None and y is not None
    
    def test_exact_boundary_longitude_180(self):
        """Test longitude = 180."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        # Should not raise an error
        x, y = transformer.to_dataset(0.0, 180.0)
        assert x is not None and y is not None
    
    def test_exact_boundary_longitude_minus_180(self):
        """Test longitude = -180."""
        from src.service.coordinate_transformer import CoordinateTransformer
        from rasterio.crs import CRS
        
        transformer = CoordinateTransformer(CRS.from_string("ESRI:54009"))
        # Should not raise an error
        x, y = transformer.to_dataset(0.0, -180.0)
        assert x is not None and y is not None
    
    def test_zero_density(self):
        """Test area with zero population."""
        # Should return 0.0, not raise an error
        pass
    
    def test_nodata_value(self):
        """Test pixel with nodata value."""
        # Should return 0.0, not raise an error
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])