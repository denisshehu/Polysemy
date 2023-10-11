from utils.functions import *
from utils.variables import *


# plt.style.use('science')

def visualize_dimension(point_cloud, figure_name, advanced=False, colormap='plasma', elev=None,
                        azim=None, roll=None, hide_xticks=False, hide_yticks=False, hide_zticks=False):
    points = point_cloud.get_query_points()
    values = np.array([query.intrinsic_dimension for query in point_cloud.queries])
    plot_3d_scatterplot(points, values, colormap, 'Intrinsic dimension', elev, azim, roll, hide_xticks, hide_yticks,
                        hide_zticks, f'{figure_name}_3d')

    if advanced:
        for query in point_cloud.queries:
            for estimates, type in [(query.initial_intrinsic_dimension_estimates, 'initial'), (query.filtered_intrinsic_dimension_estimates, 'filtered')]:
                x, y = list(estimates.keys()), list(estimates.values())
                plot_line_plot(x, y, 'Neighborhood size', 'Intrinsic dimension', f'{figure_name}_{query.identifier}_{type}')

    plot_scatterplot(values, np.ones(values.shape), 'Intrinsic dimension', None, True, f'{figure_name}_2d')


def plot_3d_scatterplot(points, values, colormap, colorbar_label, elev, azim, roll, hide_xticks, hide_yticks,
                        hide_zticks, figure_name):
    dimension = points.shape[-1]
    if dimension < 4:
        points = add_extra_dimensions(points, 3)
        if dimension < 3:
            elev = -90 if elev is None else elev
            azim = 0 if azim is None else azim
            hide_zticks = True
        _plot_3d_scatterplot(points, values, colormap, colorbar_label, elev, azim, roll, hide_xticks, hide_yticks,
                             hide_zticks, figure_name)


def _plot_3d_scatterplot(points, values, colormap, colorbar_label, elev, azim, roll, hide_xticks, hide_yticks,
                         hide_zticks, figure_name):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=values, cmap=colormap)
    fig.colorbar(scatter, label=colorbar_label)
    ax.set_aspect('equal')
    ax.view_init(elev=elev, azim=azim, roll=roll)

    if hide_xticks:
        ax.set_xticks([])
    if hide_yticks:
        ax.set_yticks([])
    if hide_zticks:
        ax.set_zticks([])

    figure_path = os.path.join(results_directory, f'{figure_name}.png')
    plt.savefig(figure_path, dpi=300)


def plot_scatterplot(x, y, xlabel, ylabel, hide_yticks, figure_name):
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot()
    ax.scatter(x, y, c='black')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if hide_yticks:
        ax.set_yticks([])

    figure_path = os.path.join(results_directory, f'{figure_name}.png')
    plt.savefig(figure_path, dpi=300)


def plot_line_plot(x, y, xlabel, ylabel, figure_name):
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot()
    ax.plot(x, y, c='black', linestyle='-')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    figure_path = os.path.join(results_directory, f'{figure_name}.png')
    plt.savefig(figure_path, dpi=300)
