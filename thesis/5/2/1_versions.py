from models.point_cloud import *
from methods.tardis import *
from methods.euclidicity_versions.euclidicity_no_scaling_no_filtering import calculate as calculate_original
from methods.euclidicity_versions.euclidicity_no_scaling_dynamic_filtering import calculate as calculate_filtered
from methods.euclidicity import calculate
from methods.intrinsic_dimension_estimators.pid_versions.pid_no_scaling_no_filtering import estimate as estimate_original
from methods.intrinsic_dimension_estimators.pid import estimate

n = 20000
intrinsic_dimension = 2
r = 1
seed = 1
ambient_dimension = intrinsic_dimension
n_queries = 1000
neighborhood_size = 200
maximum_dimension = 3
n_steps = 10

iterations = [('original', estimate_original, calculate_original), ('filtered', estimate, calculate_filtered),
              ('scaled', estimate, calculate), ('no_estimation', None, calculate)]

for string, estimation_method, calculation_method in iterations:
    points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
    point_cloud = PointCloud()
    point_cloud.random_constructor(points, n_queries, seed)

    if estimation_method is None:
        for query in point_cloud.queries:
            query.intrinsic_dimension = intrinsic_dimension
    else:
        estimation_method(point_cloud, neighborhood_size, maximum_dimension, n_steps=n_steps, filename_prefix=string)
    visualize_dimension(point_cloud, string, include_individual_plots=False)

    calculation_method(point_cloud, neighborhood_size, n_steps=n_steps, filename_prefix=string)
    visualize_euclidicity(point_cloud, string)
