from utils.functions import *
from utils.variables import *


# plt.style.use(['science', 'high-contrast'])


def visualize_topological_polysemy(point_cloud, figure_name_prefix, colormap=None, elev=None, azim=None, roll=None,
                                   hide_x_tick_labels=True, hide_y_tick_labels=True, hide_z_tick_labels=True):
    attribute = 'topological_polysemy'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, elev, azim, roll,
                         hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels)


def visualize_classification(point_cloud, figure_name_prefix, colormap=None, elev=None, azim=None, roll=None,
                             hide_x_tick_labels=True, hide_y_tick_labels=True, hide_z_tick_labels=True):
    attribute = 'classification'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, elev, azim, roll,
                         hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels)


def visualize_euclidicity(point_cloud, figure_name_prefix, colormap=None, elev=None, azim=None, roll=None,
                          hide_x_tick_labels=True, hide_y_tick_labels=True, hide_z_tick_labels=True):
    attribute = 'euclidicity'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, elev, azim, roll,
                         hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels)


def visualize_dimension(point_cloud, figure_name_prefix, include_individual_plots=True, colormap=None,
                        elev=None, azim=None, roll=None, hide_x_tick_labels=True, hide_y_tick_labels=True,
                        hide_z_tick_labels=True):
    attribute = 'intrinsic_dimension'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, elev, azim, roll,
                         hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels)

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
                x_label = 'Neighborhood size'
                y_label = attribute.replace('_', ' ').capitalize()
                figure_name = f'{figure_name_prefix}_{q}_{estimates_type}_{attribute}'
                figure_size = (9, 3)

                plot_line_plot(x, y, x_label, y_label, min_x, max_x, min_y, max_y, figure_name, figure_size)


def _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, elev, azim, roll,
                         hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels):
    points = point_cloud.get_query_points()
    attribute_values = np.array([getattr(query, attribute) for query in point_cloud.queries])
    label = attribute.replace('_', ' ').capitalize()

    # 3D plot
    color_bar_label = label
    figure_name = f'{figure_name_prefix}_3d_plot_{attribute}'
    figure_size = (3, 3)

    plot_3d_scatterplot(points, attribute_values, colormap, color_bar_label, elev, azim, roll,
                        hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, figure_name, figure_size)

    # Summary plot
    are_words_none = None in [query.word for query in point_cloud.queries]
    y = np.array(
        [query.word_type.replace(' ', '\n') for query in point_cloud.queries]) if not are_words_none else np.ones(
        attribute_values.shape)
    x_label = label
    y_label = 'Word type' if not are_words_none else None
    figure_name = f'{figure_name_prefix}_plot_summary_{attribute}'
    figure_size = (9, 3)

    plot_scatterplot(attribute_values, y, x_label, y_label, are_words_none, figure_name, figure_size)


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
    figure_size = (9, 3)
    plot_multiple_scatterplots(xs, ys, labels, colors, figure_name=figure_name, figure_size=figure_size)


def plot_3d_scatterplot(points, values=None, colormap=None, color_bar_label=None, elev=None, azim=None, roll=None,
                        hide_x_tick_labels=False, hide_y_tick_labels=False, hide_z_tick_labels=False,
                        hide_color_bar=False, figure_context=None, figure_name=None, figure_size=None):
    if figure_context is None:
        figure_context = list()
    dimension = points.shape[-1]

    if dimension < 4:
        points = add_extra_dimensions(points, 3)

        if dimension < 3:
            elev = -90 if elev is None else elev
            azim = 0 if azim is None else azim
            hide_z_tick_labels = True

        _plot_3d_scatterplot(points, values, colormap, color_bar_label, elev, azim, roll,
                             hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                             figure_context, figure_name, figure_size)


def _plot_3d_scatterplot(points, values, colormap, color_bar_label, elev, azim, roll,
                         hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                         figure_context, figure_name, figure_size):
    with plt.style.context(figure_context):
        fig = plt.figure(figsize=figure_size)
        ax = fig.add_subplot(projection='3d')
        scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=values, cmap=colormap)
        ax.set_aspect('equal')
        ax.view_init(elev=elev, azim=azim, roll=roll)

        if hide_x_tick_labels:
            ax.set_xticklabels([])
        if hide_y_tick_labels:
            ax.set_yticklabels([])
        if hide_z_tick_labels:
            ax.set_zticklabels([])
        if not hide_color_bar:
            fig.colorbar(scatter, label=color_bar_label)

        if figure_name is not None:
            figure_path = os.path.join(results_directory, f'{figure_name}.png')
            plt.savefig(figure_path, dpi=300)
            print(plt.gcf().get_size_inches())
            plt.close()
        else:
            plt.show()


def plot_scatterplot(x, y, x_label=None, y_label=None, min_x=None, max_x=None, min_y=None, max_y=None, point_sizes=None,
                     hide_y_tick_labels=False, figure_context=None, figure_name=None, figure_size=None):
    if figure_context is None:
        figure_context = list()

    with plt.style.context(figure_context):
        fig, ax = plt.subplots(figsize=figure_size)

        if point_sizes is None:
            ax.scatter(x, y, c='k')
        else:
            ax.scatter(x, y, s=point_sizes, c='k')

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
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

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

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
                   figure_name=None, figure_size=None):
    fig, ax = plt.subplots(figsize=figure_size)
    ax.plot(x, y, 'k:o', markersize=4)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    if figure_name is not None:
        figure_path = os.path.join(results_directory, f'{figure_name}.png')
        plt.savefig(figure_path, dpi=300)
        plt.close()
    else:
        plt.show()
