from methods.intrinsic_dimension_estimators.pid_versions.pid_scaling_no_filtering import \
    estimate as estimate_no_filtering
from methods.intrinsic_dimension_estimators.pid_versions.pid_scaling_dynamic_filtering import \
    estimate as estimate_dynamic_filtering
from methods.intrinsic_dimension_estimators.pid_versions.pid_scaling_constant_filtering import \
    estimate as estimate_constant_filtering
from models.point_cloud import *

n = 20000
intrinsic_dimension = 2
r = 1
seed = 1
ambient_dimension = 300

pid_versions = [('no_filtering', estimate_no_filtering), ('dynamic_filtering', estimate_dynamic_filtering),
                ('constant_filtering', estimate_constant_filtering)]
neighborhood_sizes = [20 * (i + 1) for i in range(20)]
maximum_dimension = intrinsic_dimension + 1
n_steps = 10

estimations = [[], [], []]
for i, (string, estimation_method) in enumerate(pid_versions):
    for neighborhood_size in neighborhood_sizes:
        prefix = f'{i + 1}_{string}_k{neighborhood_size}'

        points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
        point_cloud = PointCloud()
        point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))

        estimation_method(point_cloud, neighborhood_size, maximum_dimension, n_steps=n_steps, filename_prefix=prefix)
        # point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))
        estimations[i].append([query.intrinsic_dimension for query in point_cloud.queries][0])

yn_labels = [pid_version[0].replace('_', ' ').capitalize() for pid_version in pid_versions]
x_label, y_label = 'Neighborhood cardinality', 'Estimated intrinsic dimension'
padding = 0.05
x_padding = padding * (neighborhood_sizes[-1] - neighborhood_sizes[0])
min_x, max_x = neighborhood_sizes[0] - x_padding, neighborhood_sizes[-1] + x_padding
min_y = 0
figure_size = (10, 4.8)
plot_line_plot(neighborhood_sizes, estimations[0], estimations[1], estimations[2],
               yn_labels[0], yn_labels[1], yn_labels[2], x_label, y_label, min_x, max_x, min_y, a=intrinsic_dimension,
               figure_name='pid_exploration', figure_size=figure_size)
