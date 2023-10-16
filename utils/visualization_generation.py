from utils.functions import *
from utils.variables import *

plt.style.use('science')


def visualize_dimension(point_cloud, figure_name_prefix, include_individual_plots=False, colormap=None,
                        elev=None, azim=None, roll=None, hide_x_ticks=True, hide_y_ticks=True, hide_z_ticks=True):
    points = point_cloud.get_query_points()
    intrinsic_dimensions = np.array([query.intrinsic_dimension for query in point_cloud.queries])

    plot_3d_scatterplot(points, intrinsic_dimensions, colormap, 'Intrinsic dimension', elev, azim, roll,
                        hide_x_ticks, hide_y_ticks, hide_z_ticks, f'{figure_name_prefix}_3d', (3, 3))

    words = [query.word for query in point_cloud.queries]
    are_words_none = None in words
    y = np.array(
        [query.word_type.replace(' ', '\n') for query in point_cloud.queries]) if not are_words_none else np.ones(
        intrinsic_dimensions.shape)
    y_label = 'Word type' if not are_words_none else None
    plot_scatterplot(intrinsic_dimensions, y, 'Intrinsic dimension', y_label, are_words_none,
                     f'{figure_name_prefix}_intrinsic_dimension_summary', (9, 3))  # , (15, 5))

    if include_individual_plots:
        for query in point_cloud.queries:
            min_x, max_x, min_y, max_y = None, None, None, None

            for estimates, estimates_type in [(query.initial_intrinsic_dimension_estimates, 'initial'),
                                              (query.filtered_intrinsic_dimension_estimates, 'filtered')]:
                x, y = list(estimates.keys()), list(estimates.values())

                if estimates_type == 'initial':
                    min_x, max_x, min_y, max_y = min(x), max(x), min(y), max(y)

                q = query.word if not are_words_none else query.identifier
                plot_line_plot(x, y, 'Neighborhood size', 'Intrinsic dimension', min_x, max_x,
                               min_y, max_y, f'{figure_name_prefix}_{q}_{estimates_type}_estimates', (9, 3))  # , (15, 5))


def plot_3d_scatterplot(points, values=None, colormap=None, colorbar_label=None, elev=None, azim=None, roll=None,
                        hide_x_ticks=False, hide_y_ticks=False, hide_z_ticks=False, figure_name=None, figure_size=None):
    dimension = points.shape[-1]

    if dimension < 4:
        points = add_extra_dimensions(points, 3)

        if dimension < 3:
            elev = -90 if elev is None else elev
            azim = 0 if azim is None else azim
            hide_z_ticks = True

        _plot_3d_scatterplot(points, values, colormap, colorbar_label, elev, azim, roll,
                             hide_x_ticks, hide_y_ticks, hide_z_ticks, figure_name, figure_size)


def _plot_3d_scatterplot(points, values, colormap, colorbar_label, elev, azim, roll, hide_x_ticks, hide_y_ticks,
                         hide_z_ticks, figure_name, figure_size):
    fig = plt.figure(figsize=figure_size)
    ax = fig.add_subplot(projection='3d')
    scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=values, cmap=colormap)
    fig.colorbar(scatter, label=colorbar_label)
    ax.set_aspect('equal')
    ax.view_init(elev=elev, azim=azim, roll=roll)

    if hide_x_ticks:
        ax.set_xticklabels([])
    if hide_y_ticks:
        ax.set_yticklabels([])
    if hide_z_ticks:
        ax.set_zticklabels([])

    if figure_name is not None:
        figure_path = os.path.join(results_directory, f'{figure_name}.png')
        plt.savefig(figure_path, dpi=300)
        plt.close()
    else:
        plt.show()


def plot_scatterplot(x, y, x_label=None, y_label=None, hide_y_ticks=False, figure_name=None, figure_size=None):
    fig, ax = plt.subplots(figsize=figure_size)
    ax.scatter(x, y, c='black')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    if hide_y_ticks:
        ax.set_yticks([])

    if figure_name is not None:
        figure_path = os.path.join(results_directory, f'{figure_name}.png')
        plt.savefig(figure_path, dpi=300)
        plt.close()
    else:
        plt.show()


def plot_line_plot(x, y, x_label=None, y_label=None, min_x=None, max_x=None, min_y=None, max_y=None,
                   figure_name=None, figure_size=None):
    fig, ax = plt.subplots(figsize=figure_size)
    ax.plot(x, y, 'k--o')
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
