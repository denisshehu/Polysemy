import matplotlib.colors

from utils.sample_generation import *
from utils.visualization_generation import *


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:(i + 2)], 16) / 255.0 for i in (0, 2, 4))


n = 10000
intrinsic_dimension = 2
r = 1
seed = 1
ambient_dimension = 3
figure_size = (5, 5)

blue = hex_to_rgb('#648FFF')
purple = hex_to_rgb('#785EF0')
red = hex_to_rgb('#DC267F')
orange = hex_to_rgb('#FE6100')
yellow = hex_to_rgb('#FFB000')

colors = [blue, purple, red, orange, yellow]
positions = [0.0, 0.25, 0.5, 0.75, 1.0]
colormap = matplotlib.colors.LinearSegmentedColormap.from_list('colormap', list(zip(positions, colors)))

points = sample_from_sphere(n, intrinsic_dimension, r, seed, ambient_dimension)
points = np.array([p for p in points if p[0] <= 0])
values = [p[0] for p in points]
plot_3d_scatterplot(points, values, colormap=colormap, hide_x_tick_labels=True, hide_y_tick_labels=True,
                    hide_z_tick_labels=True, hide_color_bar=True, figure_name='sphere', figure_size=figure_size)

intrinsic_dimension = 3
points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
points = np.array([p for p in points if p[0] <= 0])
values = [p[0] for p in points]
plot_3d_scatterplot(points, values, colormap=colormap, hide_x_tick_labels=True, hide_y_tick_labels=True,
                    hide_z_tick_labels=True, hide_color_bar=True, figure_name='ball', figure_size=figure_size)

n = 4000
angle_in_degrees = 30
points = sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed, ambient_dimension)
values = [p[0] for p in points]
plot_3d_scatterplot(points, values, colormap=colormap, hide_x_tick_labels=True, hide_y_tick_labels=True,
                    hide_z_tick_labels=True, hide_color_bar=True, figure_name='cones', figure_size=figure_size)

n1, n2 = 2000, 2000
r1, r2 = 1, 1
intrinsic_dimension = 2
seed1, seed2 = 1, 1
points = sample_from_intersecting_planes(n1, r1, n2, r2, intrinsic_dimension, seed1, seed2, ambient_dimension)
points = np.array([p for p in points if p[1] >= 0])
values = [-1 * p[1] for p in points]
plot_3d_scatterplot(points, values, colormap=colormap, hide_x_tick_labels=True, hide_y_tick_labels=True,
                    hide_z_tick_labels=True, hide_color_bar=True, figure_name='planes', figure_size=figure_size)
