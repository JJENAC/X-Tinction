"Custom exceptions for population density API."

class PopulationDensityError(Exception):
    "Base exception for population density operations."
    pass


class CoordinateValidationError(PopulationDensityError):
    "Raised when coordinate validation fails."
    pass


class CoordinateTransformationError(PopulationDensityError):
    "Raised when coordinate transformation fails."
    pass


class DatasetError(PopulationDensityError):
    "Raised when there's an issue with the dataset."
    pass


class OutOfBoundsError(PopulationDensityError):
    "Raised when coordinates are outside the dataset bounds."
    pass