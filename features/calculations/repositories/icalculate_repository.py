from abc import ABC, abstractmethod


class ICalculateRepository(ABC):
    @abstractmethod
    def clusterize(self, data: list[list], eps: float=1.4, extra_type: str='none') -> list[list[list]]:
        pass

    @abstractmethod
    def find_centroid_min_dist_sum(self, cluster: list[list]) -> list[int, int]:
        pass

    @abstractmethod
    def find_centroid_arithmetic_mean(self, cluster: list[list]) -> list[int, int]:
        pass

    @abstractmethod
    def find_anti_centroid_max_dist_sum(self, cluster: list[list]) -> list[int, int]:
        pass
