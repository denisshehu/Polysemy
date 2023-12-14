from models.point_cloud import *
from methods.gad import *

n1, n2 = 20000, 20000
intrinsic_dimension = 2
r1, r2 = 1, 1
seed = 1
ambient_dimension = intrinsic_dimension + 1
neighborhood_size = 400
min_to_max_s_ratio = 1
r_to_s_ratio = 0.7
n_steps = 1
n_queries = 10000
prefix = '5_4_2'

points = sample_from_intersecting_planes(n1, r1, n2, r2, intrinsic_dimension, seed, seed, ambient_dimension)
point_cloud = PointCloud()
point_cloud.random_constructor(points, n_queries, seed)

for query in point_cloud.queries:
    query.intrinsic_dimension = intrinsic_dimension
detect(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, filename_prefix=prefix)

new_queries = list()
for query in point_cloud.queries:
    if query.point[1] >= 0:
        new_queries.append(query)
point_cloud.queries = new_queries
visualize_classification(point_cloud, prefix)
