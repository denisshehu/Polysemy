from utils.functions import *
from utils.variables import *

plt.rcParams.update({
    'font.family': 'serif',
    'text.usetex': True,
    'text.latex.preamble': r"""
        \usepackage{libertine}
        \usepackage{libertinust1math}
    """,
})
label_font_size = 14


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:(i + 2)], 16) / 255.0 for i in (0, 2, 4))


blue = hex_to_rgb('#648FFF')
purple = hex_to_rgb('#785EF0')
red = hex_to_rgb('#DC267F')
orange = hex_to_rgb('#FE6100')
yellow = hex_to_rgb('#FFB000')
my_colormap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'my_colormap', list(zip([0.0, 0.25, 0.5, 0.75, 1.0], [blue, purple, red, orange, yellow])))


def get_label(attribute):
    if attribute == 'topological_polysemy' or attribute == 'classification':
        return attribute.replace('_', ' ').capitalize()
    elif attribute == 'euclidicity':
        return 'Euclidicity score'
    elif attribute == 'intrinsic_dimension':
        return 'Estimated intrinsic dimension'


def visualize_topological_polysemy(point_cloud, figure_name_prefix, colormap=my_colormap, color_bar_min=None,
                                   color_bar_max=None, elev=None, azim=None, roll=None, hide_x_tick_labels=True,
                                   hide_y_tick_labels=True, hide_z_tick_labels=True, hide_color_bar=False):
    attribute = 'topological_polysemy'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                         elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar)


def visualize_classification(point_cloud, figure_name_prefix, colormap=my_colormap, color_bar_min=-0.2,
                             color_bar_max=2.2, elev=None, azim=None, roll=None, hide_x_tick_labels=True,
                             hide_y_tick_labels=True, hide_z_tick_labels=True, hide_color_bar=False):
    attribute = 'classification'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                         elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar)


def visualize_euclidicity(point_cloud, figure_name_prefix, colormap=my_colormap, color_bar_min=None,
                          color_bar_max=None, elev=None, azim=None, roll=None, hide_x_tick_labels=True,
                          hide_y_tick_labels=True, hide_z_tick_labels=True, hide_color_bar=False):
    attribute = 'euclidicity'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                         elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar)


def visualize_dimension(point_cloud, figure_name_prefix, include_individual_plots=True, known_dimension=None,
                        colormap=my_colormap, color_bar_min=None, color_bar_max=None, elev=None, azim=None, roll=None,
                        hide_x_tick_labels=True, hide_y_tick_labels=True, hide_z_tick_labels=True,
                        hide_color_bar=False):
    attribute = 'intrinsic_dimension'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                         elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar)

    # Individual plots
    if include_individual_plots:
        for query in point_cloud.queries:
            min_x, max_x, min_y, max_y = None, None, None, None
            for estimates, estimates_type in [(query.initial_intrinsic_dimension_estimates, 'initial'),
                                              (query.filtered_intrinsic_dimension_estimates, 'filtered')]:

                x, y = list(estimates.keys()), list(estimates.values())
                if estimates_type == 'initial':
                    min_x, max_x, min_y, max_y = min(x), max(x), min(y), max(y)

                are_words_none = None in [query.word for query in point_cloud.queries]
                q = query.word if not are_words_none else query.identifier
                x_label = 'Neighborhood cardinality'
                y_label = get_label(attribute)
                figure_name = f'{figure_name_prefix}_{q}_{estimates_type}_{attribute}'
                figure_size = (10, 4.8)

                plot_line_plot(x, y, x_label, y_label, min_x, max_x, min_y, max_y,
                               a=known_dimension, figure_name=figure_name, figure_size=figure_size)


def _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                         elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar):
    points = point_cloud.get_query_points()
    attribute_values = np.array([getattr(query, attribute) for query in point_cloud.queries])
    label = get_label(attribute)

    # 3D plot
    color_bar_label = label
    figure_name = f'{figure_name_prefix}_3d_plot_{attribute}'
    # figure_size = (3, 3)

    plot_3d_scatterplot(points, attribute_values, colormap, color_bar_label, color_bar_min, color_bar_max,
                        elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                        figure_name)

    # Summary plot
    are_words_none = None in [query.word for query in point_cloud.queries]
    y = np.array(
        [query.word_type.replace(' ', '\n') for query in point_cloud.queries]) if not are_words_none else np.ones(
        attribute_values.shape)
    x_label = label
    y_label = 'Word type' if not are_words_none else None
    figure_name = f'{figure_name_prefix}_plot_summary_{attribute}'
    figure_size = None  # (9, 3)

    plot_scatterplot(attribute_values, y, x_label, y_label, color_bar_min, color_bar_max,
                     hide_y_tick_labels=are_words_none, figure_name=figure_name, figure_size=figure_size)


def visualize_neighborhood_eigenvalues(point_cloud, figure_name_prefix):
    xs, ys, labels, colors = list(), list(), list(), list()

    for query in point_cloud.queries:
        y = query.neighborhood_eigenvalues
        x = range(len(y))
        label = query.word_type
        if label == 'Monoseme':
            color = 'red'
        elif label == 'Inter-class polyseme':
            color = 'green'
        elif label == 'Intra-class polyseme':
            color = 'blue'
        else:
            color = None

        xs.append(x)
        ys.append(y)
        labels.append(label)
        colors.append(color)

    figure_name = f'{figure_name_prefix}_eigenvalues'
    figure_size = None  # (9, 3)
    plot_multiple_scatterplots(xs, ys, labels, colors, figure_name=figure_name, figure_size=figure_size)


def plot_3d_scatterplot(points, values=None, colormap=my_colormap, color_bar_label=None,
                        color_bar_min=None, color_bar_max=None, elev=None, azim=None, roll=None,
                        hide_x_tick_labels=False, hide_y_tick_labels=False, hide_z_tick_labels=False,
                        hide_color_bar=False, figure_name=None, figure_size=None):
    dimension = points.shape[-1]

    if dimension < 4:
        points = add_extra_dimensions(points, 3)

        if dimension < 3:
            elev = -90 if elev is None else elev
            azim = 0 if azim is None else azim
            hide_z_tick_labels = True

        _plot_3d_scatterplot(points, values, colormap, color_bar_label, color_bar_min, color_bar_max, elev, azim, roll,
                             hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                             figure_name, figure_size)


def _plot_3d_scatterplot(points, values, colormap, color_bar_label, color_bar_min, color_bar_max, elev, azim, roll,
                         hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                         figure_name, figure_size):
    fig = plt.figure(figsize=figure_size)
    ax = fig.add_subplot(projection='3d')

    if type(values[0]) is np.str_:
        hide_color_bar = True

        colors = [blue, purple, red]
        positions = [0.0, 0.5, 1.0]
        colormap = matplotlib.colors.LinearSegmentedColormap.from_list('colormap', list(zip(positions, colors)))

        new_values = list()
        for value in values:
            if value == 'boundary':
                new_values.append(0)
            elif value == 'regular':
                new_values.append(1)
            else:
                new_values.append(2)
        values = new_values

        labels = ['boundary', 'regular', 'singular']
        dummy = [ax.scatter([], [], ls='-', c=c) for c in colors]
        ax.legend(dummy, labels, loc='upper right')

    scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=values, cmap=colormap)
    scatter.set_clim(vmin=color_bar_min, vmax=color_bar_max)
    ax.set_aspect('equal')
    ax.view_init(elev=elev, azim=azim, roll=roll)

    if hide_x_tick_labels:
        ax.set_xticklabels([])
    if hide_y_tick_labels:
        ax.set_yticklabels([])
    if hide_z_tick_labels:
        ax.set_zticklabels([])
    if not hide_color_bar:
        fig.colorbar(scatter).set_label(color_bar_label, fontsize=label_font_size)

    if figure_name is not None:
        figure_path = os.path.join(results_directory, f'{figure_name}.png')
        plt.savefig(figure_path, dpi=300)
        plt.close()
    else:
        plt.show()


def plot_scatterplot(x, y, x_label=None, y_label=None, min_x=None, max_x=None, min_y=None, max_y=None, point_sizes=None,
                     hide_y_tick_labels=False, figure_name=None, figure_size=None):
    fig, ax = plt.subplots(figsize=figure_size)

    if point_sizes is None:
        ax.scatter(x, y, c='k')
    else:
        ax.scatter(x, y, s=point_sizes, c='k')

    ax.set_xlabel(x_label, fontsize=label_font_size)
    ax.set_ylabel(y_label, fontsize=label_font_size)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    if hide_y_tick_labels:
        ax.set_yticklabels([])

    if figure_name is not None:
        figure_path = os.path.join(results_directory, f'{figure_name}.png')
        plt.savefig(figure_path, dpi=300)
        plt.close()
    else:
        plt.show()


def plot_multiple_scatterplots(xs, ys, labels, colors, x_label=None, y_label=None, figure_name=None, figure_size=None):
    fig, ax = plt.subplots(figsize=figure_size)

    for x, y, label, color in zip(xs, ys, labels, colors):
        ax.scatter(x, y, 10, label=label, color=color)

    ax.set_xlabel(x_label, fontsize=label_font_size)
    ax.set_ylabel(y_label, fontsize=label_font_size)

    ax.legend()
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(unique.values(), unique.keys())

    if figure_name is not None:
        figure_path = os.path.join(results_directory, f'{figure_name}.png')
        plt.savefig(figure_path, dpi=300)
        plt.close()
    else:
        plt.show()


def plot_line_plot(x, y, x_label=None, y_label=None, min_x=None, max_x=None, min_y=None, max_y=None,
                   use_x_log_scale=False, use_y_log_scale=False, plot_y_equals_x=False, a=None,
                   figure_name=None, figure_size=None):
    fig, ax = plt.subplots(figsize=figure_size)

    if use_x_log_scale:
        plt.xscale('log')
    if use_y_log_scale:
        plt.yscale('log')

    if plot_y_equals_x:
        ax.plot([min_x, max_x], [min_y, max_y], linestyle='-', color=red)

    if a is not None:
        ax.plot([min_x, max_x], [a, a], linestyle='-', color=red)

    ax.plot(x, y, 'k:o', markersize=4)
    ax.set_xlabel(x_label, fontsize=label_font_size)
    ax.set_ylabel(y_label, fontsize=label_font_size)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    if figure_name is not None:
        figure_path = os.path.join(results_directory, f'{figure_name}.png')
        plt.savefig(figure_path, dpi=300)
        plt.close()
    else:
        plt.show()

    # if type(values[0]) is not np.str_:
    #     scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=values, cmap=colormap)
    #
    #     if not hide_color_bar:
    #         fig.colorbar(scatter).set_label(color_bar_label, fontsize=label_font_size)
    #
    # else:
    #     regular = np.array([points[i] for i in range(np.shape(points)[0]) if values[i] == 'regular'])
    #     boundary = np.array([points[i] for i in range(np.shape(points)[0]) if values[i] == 'boundary'])
    #     singular = np.array([points[i] for i in range(np.shape(points)[0]) if values[i] == 'singular'])
    #
    #     if np.shape(boundary)[0] > 0:
    #         ax.scatter(boundary[:, 0], boundary[:, 1], boundary[:, 2], c=purple, label='boundary')
    #     if np.shape(regular)[0] > 0:
    #         ax.scatter(regular[:, 0], regular[:, 1], regular[:, 2], c=blue, label='regular')
    #     if np.shape(singular)[0] > 0:
    #         ax.scatter(singular[:, 0], singular[:, 1], singular[:, 2], c=red, label='singular')
    #     ax.legend()
