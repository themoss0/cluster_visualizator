import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull
import io

def get_convex_hull(points):
    if len(points) < 3:
        return None
    pts = np.array(points)
    try:
        hull = ConvexHull(pts)
        return pts[hull.vertices]
    except Exception:
        return None

def generate_overview_plot(points, labels, has_planets, stats_list=None):
    fig, ax = plt.subplots(figsize=(10, 8))
    unique_labels = sorted(set(labels) - {-1})
    cmap = plt.cm.get_cmap('tab10', len(unique_labels))
    color_map = {lab: cmap(i) for i, lab in enumerate(unique_labels)}
    color_map[-1] = 'gray'
    
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    colors = [color_map[lab] for lab in labels]
    marker = '*' if has_planets else 'o'
    size = 30 if has_planets else 20
    
    ax.scatter(xs, ys, c=colors, s=size, marker=marker, edgecolors='none', alpha=0.8)
    
    # Легенда
    handles = []
    for lab in unique_labels:
        handles.append(plt.Line2D([0], [0], marker=marker, color='w',
                                  markerfacecolor=color_map[lab],
                                  markersize=8, label=f'Кластер {lab}'))
    if -1 in labels:
        handles.append(plt.Line2D([0], [0], marker=marker, color='w',
                                  markerfacecolor='gray', markersize=8, label='Шум'))
    ax.legend(handles=handles, loc='best')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Кластеризация точек (общий вид)')
    ax.autoscale(enable=True, tight=True)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return buf

def generate_cluster_zoom(points, labels, cluster_id, has_planets, stats):
    indices = [i for i, lab in enumerate(labels) if lab == cluster_id]
    if not indices:
        return None
    cluster_points = [points[i] for i in indices]
    xs = [p[0] for p in cluster_points]
    ys = [p[1] for p in cluster_points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    
    # Отступ
    dx = x_max - x_min
    dy = y_max - y_min
    margin_x = dx * 0.1 if dx > 0 else 1.0
    margin_y = dy * 0.1 if dy > 0 else 1.0
    
    fig, ax = plt.subplots(figsize=(10, 8))
    unique_labels = sorted(set(labels) - {-1})
    cmap = plt.cm.get_cmap('tab10', len(unique_labels))
    color_map = {lab: cmap(i) for i, lab in enumerate(unique_labels)}
    color_map[-1] = 'gray'
    
    xs_all = [p[0] for p in points]
    ys_all = [p[1] for p in points]
    colors_all = [color_map[lab] for lab in labels]
    marker = '*' if has_planets else 'o'
    size = 30 if has_planets else 20
    
    ax.scatter(xs_all, ys_all, c=colors_all, s=size, marker=marker, edgecolors='none', alpha=0.5)
    # Выделяем точки кластера (увеличиваем и обводим)
    sizes = np.array([size] * len(points))
    edgecolors = np.array(['none'] * len(points), dtype=object)
    sizes[indices] = size * 3
    edgecolors[indices] = 'black'
    ax.scatter(xs_all, ys_all, c=colors_all, s=sizes, marker=marker, edgecolors=edgecolors, alpha=0.9)
    
    # Выпуклая оболочка
    cluster_xy = [p[:2] for p in cluster_points]
    hull_vertices = get_convex_hull(cluster_xy)
    if hull_vertices is not None:
        poly = Polygon(hull_vertices, closed=True, edgecolor='red', facecolor='red', alpha=0.2, linewidth=2)
        ax.add_patch(poly)
    
    # Центроиды (если есть в stats)
    if stats:
        centroid_min = stats.get('centroid_min_dist_sum')
        if centroid_min:
            ax.plot(centroid_min[0], centroid_min[1], 'r+', markersize=10, mew=2, label='Центроид (мин. сумма)')
        centroid_am = stats.get('centroid_arithmetic_mean')
        if centroid_am:
            ax.plot(centroid_am[0], centroid_am[1], 'gx', markersize=10, mew=2, label='Центроид (ср.ар.)')
        anticentroid = stats.get('anticentroid_max_dist_sum')
        if anticentroid:
            ax.plot(anticentroid[0], anticentroid[1], 'b^', markersize=10, label='Антицентроид')
        ax.legend()
    
    ax.set_xlim(x_min - margin_x, x_max + margin_x)
    ax.set_ylim(y_min - margin_y, y_max + margin_y)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Кластер {cluster_id} (приближение) | Точек: {len(indices)} | Диаметр: {stats.get("diameter",0):.3f}')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return buf