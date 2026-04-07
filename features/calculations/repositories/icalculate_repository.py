from abc import ABC, abstractmethod


class ICalculateRepository(ABC):
    @abstractmethod
    def clusterize(self, data: list[list], eps: float=1.4) -> list[list[list]]:
        pass