import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull

from core.di.injection import get_calculate_service
from features.calculations.services.calculate_service import CalculateService

# ----------------------------------------------------------------------
# 3. СТАТИСТИКА И ВЫПУКЛЫЕ ОБОЛОЧКИ
# ----------------------------------------------------------------------
def cluster_statistics(points, labels, cluster_id):
    """Возвращает словарь со статистикой для указанного кластера."""
    calculate_service: CalculateService = get_calculate_service()
    indices = [i for i, lab in enumerate(labels) if lab == cluster_id]
    if not indices:
        return None
    cluster_points = [points[i] for i in indices]
    xs = [p[0] for p in cluster_points]
    ys = [p[1] for p in cluster_points]
    mean_x = np.mean(xs)
    mean_y = np.mean(ys)
    centroid_minds = calculate_service.find_centroid_min_dist_sum(cluster_points)
    centroid_am = calculate_service.find_centroid_arithmetic_mean(cluster_points)
    anticentroid_maxds = calculate_service.find_anti_centroid_max_dist_sum(cluster_points)

    # Максимальное расстояние между точками (диаметр)
    max_dist = 0.0
    n = len(cluster_points)
    for i in range(n):
        for j in range(i+1, n):
            dx = cluster_points[i][0] - cluster_points[j][0]
            dy = cluster_points[i][1] - cluster_points[j][1]
            dist = np.hypot(dx, dy)
            if dist > max_dist:
                max_dist = dist
    return {
        'cluster_id': cluster_id,
        'size': n,
        'mean_x': mean_x,
        'mean_y': mean_y,
        'diameter': max_dist,
        'centroid_min_dist_sum': centroid_minds,
        'centroid_arithmetic_mean': centroid_am,
        'anticentroid_max_dist_sum': anticentroid_maxds
    }

def get_convex_hull(points):
    """Возвращает вершины выпуклой оболочки или None, если точек < 3."""
    if len(points) < 3:
        return None
    pts = np.array(points)
    try:
        hull = ConvexHull(pts)
        return pts[hull.vertices]
    except Exception:
        return None

# ----------------------------------------------------------------------
# 4. ОСНОВНОЙ КЛАСС ДЛЯ ВИЗУАЛИЗАЦИИ И ИНТЕРАКТИВА
# ----------------------------------------------------------------------
class ClusterVisualizer:
    def __init__(self, points, labels):
        self.points = points
        self.labels = labels
        self.unique_labels = sorted(set(labels) - {-1})
        self.noise_label = -1
        # Цвета для кластеров (tab10, можно расширить)
        self.cmap = plt.cm.get_cmap('tab10', len(self.unique_labels))
        self.color_map = {lab: self.cmap(i) for i, lab in enumerate(self.unique_labels)}
        self.color_map[-1] = 'gray'  # шум (в вашем алгоритме шума нет, но оставим на всякий случай)

        # Создание фигуры и осей
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.scatter = None          # ссылка на объект scatter
        self.hull_patch = None       # полигон выпуклой оболочки
        self.current_highlight = None  # выделенный кластер (id или None)
        

        self._init_plot()
        self._connect_events()

    def _init_plot(self):
        """Исходная отрисовка всех точек."""
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        colors = [self.color_map[lab] for lab in self.labels]
        self.scatter = self.ax.scatter(xs, ys, c=colors, s=20, edgecolors='none', alpha=0.8)

        handles = []
        for lab in self.unique_labels:
            handles.append(plt.Line2D([0], [0], marker='o', color='w',
                                      markerfacecolor=self.color_map[lab],
                                      markersize=8, label=f'Кластер {lab}'))
        if self.noise_label in self.labels:
            handles.append(plt.Line2D([0], [0], marker='o', color='w',
                                      markerfacecolor='gray', markersize=8, label='Шум'))
        self.ax.legend(handles=handles, loc='best')
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Кластеризация точек (левый клик – выделить кластер, правый – сброс, R – сброс)')
        self.ax.autoscale(enable=True, tight=True)

    def _connect_events(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def reset_highlight(self):
        if self.hull_patch is not None:
            self.hull_patch.remove()
            self.hull_patch = None
        self.scatter.set_sizes([20] * len(self.points))
        self.scatter.set_edgecolors('none')
        self.current_highlight = None
        self.fig.canvas.draw_idle()

    def highlight_cluster(self, cluster_id):
        if cluster_id == self.current_highlight:
            return
        self.reset_highlight()

        indices = [i for i, lab in enumerate(self.labels) if lab == cluster_id]
        if not indices:
            return

        sizes = np.array([20] * len(self.points))
        edgecolors = np.array(['none'] * len(self.points), dtype=object)
        sizes[indices] = 80
        edgecolors[indices] = 'black'
        self.scatter.set_sizes(sizes)
        self.scatter.set_edgecolors(edgecolors)

        if cluster_id != self.noise_label:
            cluster_points = [self.points[i] for i in indices]
            hull_vertices = get_convex_hull(cluster_points)
            if hull_vertices is not None:
                poly = Polygon(hull_vertices, closed=True, edgecolor='red', facecolor='red', alpha=0.2, linewidth=2)
                self.hull_patch = self.ax.add_patch(poly)

        if cluster_id == self.noise_label:
            print(f"\n[Шум] Выделена точка шума.")
        else:
            stats = cluster_statistics(self.points, self.labels, cluster_id)
            if stats:
                print(f"\n--- Кластер {stats['cluster_id']} ---")
                print(f"Количество точек: {stats['size']}")
                print(f"Среднее X: {stats['mean_x']:.4f}")
                print(f"Среднее Y: {stats['mean_y']:.4f}")
                print(f"Диаметр (макс. расстояние): {stats['diameter']:.4f}")
                print(f"\n--- Кластер {stats['cluster_id']}: Центроиды ---")
                print(f"Центроид (мин. сумма расст.): ({stats['centroid_min_dist_sum'][0]:.4f}, {stats['centroid_min_dist_sum'][1]:.4f})")
                print(f"Центроид (ср.ариф. всех точек): ({stats['centroid_arithmetic_mean'][0]:.4f}, {stats['centroid_arithmetic_mean'][1]:.4f})")
                print(f"Антицентроид (макс. сумма расст.): ({stats['anticentroid_max_dist_sum'][0]:.4f}, {stats['anticentroid_max_dist_sum'][1]:.4f})")
            else:
                print(f"\nНе удалось вычислить статистику для кластера {cluster_id}.")

        self.current_highlight = cluster_id
        self.fig.canvas.draw_idle()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        if event.button == 1:   # левая кнопка
            click_x, click_y = event.xdata, event.ydata
            min_dist = float('inf')
            nearest_idx = None
            for i, (px, py) in enumerate(self.points):
                dist = np.hypot(px - click_x, py - click_y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_idx = i
            if nearest_idx is not None and min_dist < 0.1:
                cluster_id = self.labels[nearest_idx]
                self.highlight_cluster(cluster_id)
            else:
                print("Клик мимо точек.")
        elif event.button == 3:   # правая кнопка
            self.reset_highlight()

    def on_key(self, event):
        if event.key == 'r':
            self.reset_highlight()

    def show(self):
        plt.show()