from features.calculations.repositories.icalculate_repository import ICalculateRepository


class CalculateService:
    def __init__(self, icalculate_repository: ICalculateRepository):
        self.calculate_repository=icalculate_repository

    def clusterize(self, data:list[list], eps:float):
        """
        Разбивает точки на кластеры.

        Аргументы:

        - data: Список точек.

        - eps: Расстояние между точками при кластеризации.
        """
        return self.calculate_repository.clusterize(data, eps)