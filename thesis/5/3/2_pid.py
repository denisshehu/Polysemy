from methods.intrinsic_dimension_estimators.pid import estimate
from models.point_cloud import *

n = 20000
intrinsic_dimension_values = [i + 1 for i in range(10)]
r = 1
seed = 1
ambient_dimension = 300
neighborhood_size = 50
n_steps = 10

estimations = list()
for intrinsic_dimension in intrinsic_dimension_values:
    prefix = f'd{intrinsic_dimension}'

    points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
    point_cloud = PointCloud()
    point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))

    estimate(point_cloud, neighborhood_size, intrinsic_dimension, n_steps=n_steps, filename_prefix=prefix)
    estimations.append([query.intrinsic_dimension for query in point_cloud.queries][0])

x_label, y_label = 'Intrinsic dimension', 'Estimated intrinsic dimension'
padding = 0.2
min_x, max_x = 1 - padding, intrinsic_dimension_values[-1] + padding
min_y, max_y = 1 - padding, intrinsic_dimension_values[-1] + padding
plot_line_plot(intrinsic_dimension_values, estimations, x_label, y_label, min_x, max_x, min_y, max_y,
               plot_y_equals_x=True, figure_name='pid')
