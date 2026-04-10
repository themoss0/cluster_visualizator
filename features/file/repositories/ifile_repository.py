from abc import ABC, abstractmethod


class IFileRepository(ABC):

    @abstractmethod
    def preset_lines(self, filename: str, extra_type: str='none'):
        pass

    @abstractmethod
    def load_data(self, filename: str):
        pass

    @abstractmethod
    def load_data_with_planet(self, filename: str):
        pass
