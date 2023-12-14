import random

from methods.intrinsic_dimension_estimators.pid import estimate
from models.point_cloud import *

n = 20000
intrinsic_dimension = 2
r = 1
seed = 1
ambient_dimension = 300
neighborhood_sizes = [20 * (i + 1) for i in range(20)]
maximum_dimension = intrinsic_dimension
n_steps = 10
prefix = '5_3_pid_exploration'

estimations = list()

for neighborhood_size in neighborhood_sizes:
    filename_prefix = f'{prefix}_k{neighborhood_size}'

    points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
    point_cloud = PointCloud()
    point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))

    estimate(point_cloud, neighborhood_size, maximum_dimension, n_steps=n_steps, filename_prefix=filename_prefix)
    estimations.append([query.intrinsic_dimension for query in point_cloud.queries][0])
    # estimations.append(random.randint(0, 2))

x_label, y_label = 'Neighborhood cardinality', 'Estimated intrinsic dimension'
padding = 0.05
x_padding = padding * (neighborhood_sizes[-1] - neighborhood_sizes[0])
y_padding = padding * intrinsic_dimension
min_x, max_x = neighborhood_sizes[0] - x_padding, neighborhood_sizes[-1] + x_padding
min_y, max_y = 0 - y_padding, intrinsic_dimension + y_padding
figure_size = (10, 4.8)
plot_line_plot(neighborhood_sizes, estimations, x_label, y_label, min_x, max_x, min_y, max_y, a=intrinsic_dimension,
               figure_name=prefix, figure_size=figure_size)
