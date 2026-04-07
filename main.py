from core.di.injection import get_calculate_service, get_file_service, load_dependencies
from features.file.services.file_service import FileService
from features.view.cluster_visualizer import ClusterVisualizer


if __name__ == '__main__':
    load_dependencies()

    print('Введите название файла:')
    n = input()

    file_service = get_file_service()
    calculate_service = get_calculate_service()
    data = file_service.load_data(filename=n)

    clust = calculate_service.clusterize(data, 1.4)
    
    # Преобразуем список кластеров в массив меток для каждой точки
    labels = [-1] * len(data)   # изначально все -1 (шум)
    for cluster_id, cluster_points in enumerate(clust):
        for pt in cluster_points:
            # Находим индекс этой точки в исходном списке points
            # Поскольку точки могут быть одинаковыми, используем поиск по значению
            # Но лучше сопоставлять по объекту, но здесь мы ищем по координатам
            # Для надёжности ищем первое вхождение с такими же координатами
            # (в реальных данных точки уникальны)
            for i, orig_pt in enumerate(data):
                if orig_pt[0] == pt[0] and orig_pt[1] == pt[1] and labels[i] == -1:
                    labels[i] = cluster_id
                    break
    # Проверка: все ли точки получили метку (должны, т.к. clusterize покрывает все точки)
    if any(l == -1 for l in labels):
        print("Внимание: некоторые точки не попали в кластеры (шум).")
    
    unique_clusters = set(labels) - {-1}
    print(f"Найдено кластеров: {len(unique_clusters)}, всего точек: {len(data)}")
    for cid in sorted(unique_clusters):
        size = labels.count(cid)
        print(f"  Кластер {cid}: {size} точек")
    
    # Визуализация
    vis = ClusterVisualizer(data, labels)
    vis.show()
    vis.show()
    print(data)
    print(clust)