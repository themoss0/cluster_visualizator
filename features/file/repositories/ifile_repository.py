from abc import ABC, abstractmethod


class IFileRepository(ABC):
    @abstractmethod
    def load_data(self, filename: str):
        pass
