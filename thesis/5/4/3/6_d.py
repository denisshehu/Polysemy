import winsound

from methods.euclidicity import *
from models.point_cloud import *

n = 50 + 2
n1 = n // 2
intrinsic_dimension = 10
upper_bounds = [i for i in range(2, 11)]
r = 1
angle_in_degrees = 30
seed = 1
ambient_dimension = 300

neighborhood_size = n - 2
threshold = 0.1
min_to_max_s_ratio = 1
r_to_s_ratio = 0.5
n_steps = 1

data = [
    ('regular', sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)),
    ('cones', sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed, ambient_dimension)),
    ('planes', sample_from_intersecting_planes(n1, r, n1, r, intrinsic_dimension - 1, seed, seed,
                                               ambient_dimension))
]

summary = [[], [], []]

for upper_bound in upper_bounds:
    for i, (string, points) in enumerate(data):
        prefix = f'ub{upper_bound}_{i + 1}_{string}'

        point_cloud = PointCloud()
        point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))

        for query in point_cloud.queries:
            query.intrinsic_dimension = upper_bound

        calculate(point_cloud, neighborhood_size, threshold, min_to_max_s_ratio, r_to_s_ratio, n_steps,
                  filename_prefix=prefix)
        # point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))
        summary[i].append([query.euclidicity for query in point_cloud.queries][0])

y1_label, y2_label, y3_label = 'regular', 'singular (cones)', 'singular (planes)'
x_label = 'Intrinsic dimension'
y_label = 'Euclidicity score'
figure_name = f'summary_d{upper_bounds[0]}_{upper_bounds[-1]}'
plot_line_plot(upper_bounds, summary[0], summary[1], summary[2], y1_label, y2_label, y3_label, x_label, y_label,
               min_y=0, figure_name=figure_name)

winsound.Beep(500, 3000)
