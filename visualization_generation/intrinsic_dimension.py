import os.path

from matplotlib import pyplot as plt

from utils.utils import results_directory


def visualize(point_cloud, filename_prefix):
    queries = point_cloud.queries
    monosemes = [query for query in queries if query.n_senses == 1]
    polysemes = [query for query in queries if query not in monosemes]

    x_monosemes = [query.intrinsic_dimension for query in monosemes]
    y_monosemes = [query.n_senses for query in monosemes]

    x_polysemes = [query.intrinsic_dimension for query in polysemes]
    y_polysemes = [query.n_senses for query in polysemes]

    plt.figure(figsize=(15, 5))
    plt.scatter(x_monosemes, y_monosemes, c='black', label='Monoseme')
    plt.scatter(x_polysemes, y_polysemes, c='red', label='Polyseme')
    plt.legend()

    plt.xlabel('Intrinsic dimension estimate')
    plt.ylabel('Number of senses')
    filename_prefix = f'{filename_prefix}_' if filename_prefix is not None else ''
    figure_path = os.path.join(results_directory, f'{filename_prefix}intrinsic_dimension.png')
    plt.savefig(figure_path, dpi=300)
    plt.close()


def plot3d(point_cloud, filename_prefix):
    queries = point_cloud.queries
    x = [query.point[0] for query in queries]
    y = [query.point[1] for query in queries]
    z = [query.point[2] for query in queries]
    c = [query.intrinsic_dimension for query in queries]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(x, y, z, c=c, cmap='plasma')
    fig.colorbar(scatter, label='Intrinsic dimension estimate')
    plt.gca().set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    filename_prefix = f'{filename_prefix}_' if filename_prefix is not None else ''
    figure_path = os.path.join(results_directory, f'{filename_prefix}intrinsic_dimension.png')
    plt.savefig(figure_path, dpi=300)
    plt.close()

# def stuff(point_cloud, filename_suffix):
#     data = []
#
#     queries = point_cloud.queries
#     for query in queries:
#         first_columns = [np.array2string(query.point), query.word, query.n_senses]
#         initial_intrinsic_dimension_estimates = query.initial_intrinsic_dimension_estimates
#         estimates = [estimate for estimate in initial_intrinsic_dimension_estimates.values()]
#         data.append(first_columns + estimates)
#
#     columns = ['Point', 'Word', 'Number of senses'] + [f'Neighborhood size = {neighborhood_size}' for neighborhood_size
#                                                        in queries[0].initial_intrinsic_dimension_estimates.keys()]
#
#     dataframe = pd.DataFrame(data, columns=columns)
#     save_csv(dataframe, os.path.join(results_directory, 'test.csv'))
#
#
# def visualize(point_cloud, filename_suffix):
#     counter = 1
#     for query in point_cloud.queries:
#         initial_intrinsic_dimension_estimates = query.initial_intrinsic_dimension_estimates
#         x = initial_intrinsic_dimension_estimates.keys()
#         y = initial_intrinsic_dimension_estimates.values()
#
#         figure_name = (f"{f'{query.word}_{query.n_senses}' if query.word is not None else counter}_dimension"
#                        f"{f'_{filename_suffix}' if filename_suffix is not None else ''}")
#         plot_2d(x, y, 'Neighborhood size', 'Intrinsic dimension estimate', figure_name)
#         counter += 1
#
#
# def plot_2d(x, y, x_label, y_label, figure_name):
#     plt.figure(figsize=(15, 5))
#     plt.plot(x, y, marker='o', color='black')
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)
#     plt.savefig(os.path.join(results_directory, f'{figure_name}.png'), dpi=300)
#     plt.close()
