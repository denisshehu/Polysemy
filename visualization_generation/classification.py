import os

from matplotlib import pyplot as plt

from utils.utils import results_directory


def visualize(point_cloud, filename_prefix):
    queries = point_cloud.queries
    monosemes = [query for query in queries if query.n_senses == 1]
    polysemes = [query for query in queries if query not in monosemes]

    x_monosemes = [query.classification for query in monosemes]
    y_monosemes = [query.n_senses for query in monosemes]

    x_polysemes = [query.classification for query in polysemes]
    y_polysemes = [query.n_senses for query in polysemes]

    plt.figure(figsize=(15, 5))
    plt.scatter(x_monosemes, y_monosemes, c='black', label='Monoseme')
    plt.scatter(x_polysemes, y_polysemes, c='red', label='Polyseme')
    plt.legend()

    plt.xlabel('Classification')
    plt.ylabel('Number of senses')
    filename_prefix = f'{filename_prefix}_' if filename_prefix is not None else ''
    figure_path = os.path.join(results_directory, f'{filename_prefix}classification.png')
    plt.savefig(figure_path, dpi=300)
    plt.close()


def plot3d(point_cloud, filename_prefix):
    queries = point_cloud.queries
    x = [query.point[0] for query in queries]
    y = [query.point[1] for query in queries]
    z = [query.point[2] for query in queries]
    c = [query.classification for query in queries]
    for i in range(len(c)):
        if c[i] == 'boundary':
            c[i] = 0
        elif c[i] == 'regular':
            c[i] = 1
        else:
            c[i] = 2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(x, y, z, c=c, cmap='plasma')
    fig.colorbar(scatter, label='Classification')
    plt.gca().set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    filename_prefix = f'{filename_prefix}_' if filename_prefix is not None else ''
    figure_path = os.path.join(results_directory, f'{filename_prefix}classification.png')
    plt.savefig(figure_path, dpi=300)
    plt.close()
