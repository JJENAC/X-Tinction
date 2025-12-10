from abc import ABC, abstractmethod

class PopulationDensityProvider(ABC):
    @abstractmethod
    def get_population_density(self, h3_hex: str) -> float:
        pass
