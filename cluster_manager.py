from core.di.injection import get_calculate_service, get_file_service, load_dependencies
from features.file.services.file_service import FileService
from features.view.cluster_visualizer import cluster_statistics

load_dependencies()
calc_service = get_calculate_service()

def detect_extra_type(file_path):
    """Определяет, есть ли в файле третья колонка (планеты) по первой непустой строке."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.replace(',', '.').split()
            if len(parts) >= 3:
                # пробуем преобразовать третий элемент в число – если ошибка, значит текст
                try:
                    float(parts[2])
                    return 'none'  # три числа – скорее всего не планеты
                except ValueError:
                    return 'planet'
            else:
                return 'none'
    return 'none'

def process_file(file_path, eps=1.4):
    # Определяем тип дополнительных данных
    extra_type = detect_extra_type(file_path)

    file_service = get_file_service()
    
    points = file_service.preset_lines(file_path, extra_type=extra_type)
    if not points:
        raise ValueError("Файл не содержит точек или имеет неверный формат")
    
    # Кластеризация
    clusters = calc_service.clusterize(points, eps=eps)
    
    # Построение меток для каждой точки
    labels = [-1] * len(points)
    for cluster_id, cluster_points in enumerate(clusters):
        for pt in cluster_points:
            # Поиск индекса точки (по совпадению координат – первые два элемента)
            for i, orig in enumerate(points):
                if orig[0] == pt[0] and orig[1] == pt[1] and labels[i] == -1:
                    labels[i] = cluster_id
                    break
    # Проверка, что все точки получили метку (в вашем алгоритме все точки попадают в кластеры)
    # Но на всякий случай оставим -1 для шума (не должно быть)
    
    # Сбор статистики по каждому кластеру
    unique_clusters = set(labels) - {-1}
    stats_list = []
    for cid in sorted(unique_clusters):
        stats = cluster_statistics(points, labels, cid)
        if stats:
            stats_list.append(stats)
    
    has_planets = (extra_type == 'planet')
    return points, labels, stats_list, has_planets