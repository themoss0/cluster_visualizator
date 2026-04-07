from math import dist

from features.calculations.repositories.icalculate_repository import ICalculateRepository


class CalculateRepository(ICalculateRepository):
    def __init__(self):
        pass
    
    def clusterize(self, data: list[list], eps = 1.4):
        data_copy = [p[:] for p in data]
        clusters: list = []
        while data_copy: 
            new_cluster = [data_copy.pop(0)]
            clusters.append(new_cluster)
            for point in clusters[-1]:
                neightbours = [p1 for p1 in data_copy if dist(point, p1) < eps]
                clusters[-1].extend(neightbours)
                for p1 in neightbours: data_copy.remove(p1)
        return clusters