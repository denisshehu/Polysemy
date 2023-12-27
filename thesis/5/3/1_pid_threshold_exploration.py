from methods.intrinsic_dimension_estimators.pid_versions.pid_scaling_constant_filtering import estimate
from models.point_cloud import *

n = 20000
intrinsic_dimension = 2
r = 1
seed = 1
ambient_dimension = 300

thresholds = [0.02 * (i + 1) for i in range(10)]
neighborhood_sizes = [20 * (i + 1) for i in range(10)]
maximum_dimension = intrinsic_dimension + 1
n_steps = 10

for i, threshold in enumerate(thresholds):
    estimations = list()
    for neighborhood_size in neighborhood_sizes:
        prefix = f'threshold{threshold}_k{neighborhood_size}'

        # points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
        # point_cloud = PointCloud()
        # point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))
        #
        # estimate(point_cloud, neighborhood_size, maximum_dimension, threshold, n_steps=n_steps, filename_prefix=prefix)
        point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))
        estimations.append([query.intrinsic_dimension for query in point_cloud.queries][0])

    x_label, y_label = 'Neighborhood cardinality', 'Estimated intrinsic dimension'
    padding = 0.05
    x_padding = padding * (neighborhood_sizes[-1] - neighborhood_sizes[0])
    min_x, max_x = neighborhood_sizes[0] - x_padding, neighborhood_sizes[-1] + x_padding
    min_y, max_y = 0, 3
    figure_name = f'{i + 1}_threshold{threshold}'
    figure_size = (10, 4.8)
    plot_line_plot(neighborhood_sizes, estimations, x_label=x_label, y_label=y_label, min_x=min_x, max_x=max_x,
                   min_y=min_y, max_y=max_y, a=intrinsic_dimension, figure_name=figure_name, figure_size=figure_size)
