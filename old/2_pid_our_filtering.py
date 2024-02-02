from methods.intrinsic_dimension_estimators.pid import estimate
from models.point_cloud import *

n = 20000
intrinsic_dimension_values = [i + 1 for i in range(10)]
r = 1
seed = 1
ambient_dimension = 300

neighborhood_size = 60
thresholds = [0.0, 0.1, 0.2]
n_steps = 10

results = [[], [], []]
for i, threshold in enumerate(thresholds):
    for intrinsic_dimension in intrinsic_dimension_values:
        prefix = f'{i + 1}_t{threshold}_d{intrinsic_dimension}_k{neighborhood_size}'
        maximum_dimension = intrinsic_dimension + 1

        points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
        point_cloud = PointCloud()
        point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))
        # point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

        estimate(point_cloud, neighborhood_size, maximum_dimension, threshold=threshold, n_steps=n_steps,
                 filename_prefix=prefix)
        results[i].append([query.intrinsic_dimension for query in point_cloud.queries][0])

y1_label, y2_label, y3_label = fr'$ t = {thresholds[0]} $', fr'$ t = {thresholds[1]} $', fr'$ t = {thresholds[2]} $'
x_label, y_label = 'Intrinsic dimension', 'Estimated intrinsic dimension'
padding = 1.2
min_x, max_x = 0, intrinsic_dimension_values[-1] + padding
min_y, max_y = 0, intrinsic_dimension_values[-1] + padding
figure_size = (4, 4)
plot_line_plot(intrinsic_dimension_values, results[0], results[1], results[2], y1_label, y2_label, y3_label,
               x_label, y_label, min_x, max_x, min_y, max_y, plot_y_equals_x=True,
               figure_name='pid', figure_size=figure_size)
