from old.pid_versions.pid_scaling_no_filtering import \
    estimate as estimate_no_filtering
from models.point_cloud import *

n = 20000
intrinsic_dimension_values = [i + 1 for i in range(10)]#[i + 1 for i in range(10)]
r = 1
seed = 1
ambient_dimension = 300

neighborhood_size = 60
n_steps = 10

# pid_versions = [('no_filtering', estimate_no_filtering), ('dynamic_filtering', estimate_dynamic_filtering)]

# results = [[], []]
# for i, (string, method) in enumerate(pid_versions):
results = list()
for intrinsic_dimension in intrinsic_dimension_values:
    # prefix = f'{i + 1}_{string}_d{intrinsic_dimension}_k{neighborhood_size}'
    prefix = f'd{intrinsic_dimension}_k{neighborhood_size}'
    maximum_dimension = intrinsic_dimension + 1

    points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
    point_cloud = PointCloud()
    point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))
    # point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

    # method(point_cloud, neighborhood_size, maximum_dimension, n_steps=n_steps, filename_prefix=prefix)
    # results[i].append([query.intrinsic_dimension for query in point_cloud.queries][0])
    estimate_no_filtering(point_cloud, neighborhood_size, maximum_dimension, n_steps=n_steps, filename_prefix=prefix)
    results.append([query.intrinsic_dimension for query in point_cloud.queries][0])

# y1_label, y2_label = 'Without filtering', 'Dynamic filtering'
x_label, y_label = 'Intrinsic dimension', 'Estimated intrinsic dimension'
padding = 0.2
min_x, max_x = 0, intrinsic_dimension_values[-1] + padding
min_y, max_y = 0, intrinsic_dimension_values[-1] + padding
figure_size = (4, 4)
plot_line_plot(intrinsic_dimension_values, results,
               x_label=x_label, y_label=y_label, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y,
               plot_y_equals_x=True, figure_name='pid', figure_size=figure_size)
