import random

from models.point_cloud import *
from methods.intrinsic_dimension_estimators.pid import estimate

n = 20000
intrinsic_dimension_values = [i + 1 for i in range(10)]
r = 1
seed = 1
ambient_dimension = 300
neighborhood_size = 50
# maximum_dimension = intrinsic_dimension_values[-1]
n_steps = 10
prefix = '5_3_pid'

estimations = list()

for intrinsic_dimension in intrinsic_dimension_values:
    filename_prefix = f'{prefix}_k{neighborhood_size}_d{intrinsic_dimension}'

    points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
    point_cloud = PointCloud()
    point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))

    estimate(point_cloud, neighborhood_size, intrinsic_dimension, n_steps=n_steps, filename_prefix=filename_prefix)
    estimations.append([query.intrinsic_dimension for query in point_cloud.queries][0])
    # estimations.append(random.randint(0, 5))

x_label, y_label = 'Intrinsic dimension', 'Estimated intrinsic dimension'
padding = 0.2
min_x, max_x = 1 - padding, intrinsic_dimension_values[-1] + padding
min_y, max_y = 1 - padding, intrinsic_dimension_values[-1] + padding
plot_line_plot(intrinsic_dimension_values, estimations, x_label, y_label, min_x, max_x, min_y, max_y,
               plot_y_equals_x=True, figure_name=prefix)
