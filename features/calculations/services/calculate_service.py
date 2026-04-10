from features.calculations.repositories.icalculate_repository import ICalculateRepository


class CalculateService:
    def __init__(self, icalculate_repository: ICalculateRepository):
        self.calculate_repository=icalculate_repository

    def clusterize(self, data:list[list], eps:float, extra_type: str='none'):
        """
        Разбивает точки на кластеры.

        Аргументы:

        - data: Список точек.

        - eps: Расстояние между точками при кластеризации.
        """
        return self.calculate_repository.clusterize(data, eps, extra_type)
    

    def find_centroid_min_dist_sum(self, cluster: list[list]):
        """
        Используется, когда в условии прямо говорится о том, что **центроид** - *точка кластера, сумма расстояний от которой
        до всех остальных точек кластера минимальна*
        """
        return self.calculate_repository.find_centroid_min_dist_sum(cluster)
    

    def find_centroid_arithmetic_mean(self, cluster: list[list]):
        """
        Используется, когда в условии прямо говорится о том, что 
        **центроид** - *это среднее арифметическое координат всех точек внутри кластера*
        """
        return self.calculate_repository.find_centroid_arithmetic_mean(cluster)


    def find_anti_centroid_max_dist_sum(self, cluster: list[list]):
        """
        Используется, когда в условии прямо говорится о том, что 
        **антицентроид** - *точка кластера, сумма расстояний от которой
        до всех остальных точек кластера максимальна*
        """
        return self.calculate_repository.find_anti_centroid_max_dist_sum(cluster)