from models.point_cloud import *
from methods.topological_polysemy import *

n = 20000
n1 = n // 4
intrinsic_dimension = 3
r = 1
angle_in_degrees = 30
seed = 1
ambient_dimension = intrinsic_dimension

data = [
    ('regular', sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension), 0, 270),
    ('cones', sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed, ambient_dimension),
     0, 270),
    ('planes', sample_from_intersecting_planes(n1, r, n1, r, intrinsic_dimension - 1, seed, seed, ambient_dimension),
     None, None)
]

neighborhood_size = 100
min_to_max_s_ratio = 1
r_to_s_ratio = 0.1
n_steps = 1
n_queries = 10000
color_bar_min = None#0
color_bar_max = None#13

for i, (string, points, elev, azim) in enumerate(data):
    prefix = f'{i + 1}_{string}'

    # point_cloud = PointCloud()
    # point_cloud.random_constructor(points, n_queries, seed)
    #
    # calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, filename_prefix=prefix)
    point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

    new_queries = list()
    for query in point_cloud.queries:
        if query.point[1] >= 0:
            new_queries.append(query)
    point_cloud.queries = new_queries

    visualize_topological_polysemy(point_cloud, prefix, color_bar_min=color_bar_min, color_bar_max=color_bar_max,
                                   elev=elev, azim=azim)
