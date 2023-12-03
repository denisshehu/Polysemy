from utils.main import *


def calculate(point_cloud, distance_metric, neighborhood_size, filename_prefix=None):
    """
    :param distance_metric: 'w' for wasserstein norm, 's' for square distance, and 'm' for max distance.
    """
    _calculate(point_cloud, distance_metric, neighborhood_size)
    # save_point_cloud(point_cloud, filename_prefix)
    # visualize
    # print('Topological polysemy calculated.')


def _calculate(point_cloud, distance_metric, neighborhood_size):
    neighborhoods = point_cloud.get_neighborhoods(neighborhood_size)

    for index, (query, neighborhood) in enumerate(zip(point_cloud.queries, neighborhoods)):
        progress = f'Query point {index + 1} out of {len(point_cloud.queries)}.'
        print(progress, end='\r')

        projected_neighborhood = project_to_unit_sphere(neighborhood, query.point)
        zeroth_persistence_diagram = ripser.ripser(projected_neighborhood, maxdim=0)['dgms'][0]

        if distance_metric == 'w':
            topological_polysemy = compute_wasserstein_norm(zeroth_persistence_diagram)
        elif distance_metric == 's':
            topological_polysemy = compute_square_distance(zeroth_persistence_diagram)
        elif distance_metric == 'm':
            topological_polysemy = compute_max_distance(zeroth_persistence_diagram)
        else:
            ValueError('Distance metric not implemented.')

        query.topological_polysemy = topological_polysemy

        print(f"{len(progress) * ' '}", end='\r')


def compute_wasserstein_norm(persistence_diagram):
    persistence_diagram = persistence_diagram[:-1]
    persistence_values = persistence_diagram[:, 1] - persistence_diagram[:, 0]
    distance = sum(persistence_values) / 2
    return distance


def compute_square_distance(persistence_diagram):
    persistence_diagram = persistence_diagram[:-1]
    persistence_values = persistence_diagram[:, 1] - persistence_diagram[:, 0]
    squared_persistence_values = persistence_values ** 2
    distance = sum(squared_persistence_values) / 2
    return distance


def compute_max_distance(persistence_diagram):
    persistence_diagram = persistence_diagram[:-1]
    persistence_values = persistence_diagram[:, 1] - persistence_diagram[:, 0]
    distance = max(persistence_values)
    return distance
