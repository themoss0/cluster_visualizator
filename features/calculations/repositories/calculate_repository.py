from math import dist

from features.calculations.repositories.icalculate_repository import ICalculateRepository


class CalculateRepository(ICalculateRepository):
    def __init__(self):
        pass
    
    def clusterize(self, data: list[list], eps = 1.4, extra_type: str='none'):
        data_copy = [p[:] for p in data]
        clusters: list = []
        while data_copy: 
            new_cluster = [data_copy.pop(0)]
            clusters.append(new_cluster)
            for point in clusters[-1]:
                neightbours = [p1 for p1 in data_copy if dist([point[0], point[1]], [p1[0], p1[1]]) < eps]
                clusters[-1].extend(neightbours)
                for p1 in neightbours: data_copy.remove(p1)
        return clusters
    

    def centroid(self, cluster: list[list]) -> list:
        points = []
        for p in cluster:
            if len(p) > 2: p = p[:-1]
            sm = sum(dist(p, [p1[0], p1[1]]) for p1 in cluster)
            points.append([sm, p])
        return points

    def find_centroid_min_dist_sum(self, cluster):
        points = self.centroid(cluster)
        return min(points)[-1]

    def find_centroid_arithmetic_mean(self, cluster):
        """
        Суммируем значения всех точек по X и У, делим на количество точек
        """
        sum_x = sum_y = 0
        if len(cluster[0]) > 2:
            points = [point[:-1] for point in cluster]
        else:
            points = [point for point in cluster]
        for x, y in points:
            sum_x += x
            sum_y += y
        average_x = sum_x / len(cluster)
        average_y = sum_y / len(cluster)
        return [average_x, average_y]

    def find_anti_centroid_max_dist_sum(self, cluster):
        """
        1) Перебираем суммы дистанций всех точек (от каждой - до каждой)
        2) Добавляем в общий список массив [сумма-точка]
        3) Выводим точку с максимальной суммой до всех точек
        """
        points = self.centroid(cluster)
        return max(points)[-1]