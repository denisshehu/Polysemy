from models.point_cloud import *
from methods.euclidicity_filtered import calculate as calculate_not_scaled
from methods.euclidicity import calculate as calculate_scaled

n = 20000
intrinsic_dimension = 2
r_values = [pow(10, i) for i in range(5)]
seed = 1
ambient_dimension = 2
neighborhood_size = 50
n_steps = 10

not_scaled = list()
scaled = list()

for r in r_values:
    for string, calculation_method in [('not_scaled', calculate_not_scaled), ('scaled', calculate_scaled)]:
        prefix = f'r{r}_{string}'

        points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
        point_cloud = PointCloud()
        point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))

        for query in point_cloud.queries:
            query.intrinsic_dimension = intrinsic_dimension

        calculation_method(point_cloud, neighborhood_size, n_steps=n_steps, filename_prefix=prefix)

        if string == 'not_scaled':
            not_scaled.append([query.euclidicity for query in point_cloud.queries])
        else:
            scaled.append([query.euclidicity for query in point_cloud.queries])

x_label, y_label = 'Radius', 'Euclidicity score'
min_y, max_y = 0, 0.4
plot_line_plot(r_values, not_scaled, x_label, y_label, use_x_log_scale=True, figure_name='not_scaled')
plot_line_plot(r_values, scaled, x_label, y_label, min_y=min_y, max_y=max_y, use_x_log_scale=True, figure_name='scaled')
