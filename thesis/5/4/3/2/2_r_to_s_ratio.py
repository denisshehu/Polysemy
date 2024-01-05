from models.point_cloud import *
from methods.euclidicity import *

n1, n2 = 5000, 5000
intrinsic_dimension = 2
r1, r2 = 1, 1
seed1, seed2 = 1, 1
ambient_dimension = intrinsic_dimension + 1
neighborhood_size = 100
min_to_max_s_ratio = 1
r_to_s_ratios = [0 + 0.1 * i for i in range(10)]
n_steps = 1
n_queries = 10000
color_bar_min = 0
color_bar_max = 0.8

for r_to_s_ratio in r_to_s_ratios:
    prefix = f'{r_to_s_ratio:.1f}'

    # points = sample_from_intersecting_planes(n1, r1, n2, r2, intrinsic_dimension, seed1, seed2, ambient_dimension)
    # point_cloud = PointCloud()
    # point_cloud.random_constructor(points, n_queries, seed1)
    #
    # for query in point_cloud.queries:
    #     query.intrinsic_dimension = intrinsic_dimension
    #
    # calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, filename_prefix=prefix)
    point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

    new_queries = list()
    for query in point_cloud.queries:
        if query.point[1] >= 0:
            new_queries.append(query)
    point_cloud.queries = new_queries

    visualize_euclidicity(point_cloud, prefix, color_bar_min=color_bar_min, color_bar_max=color_bar_max)