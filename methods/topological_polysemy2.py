from utils.main import *


def calculate(point_cloud, distance_metric, neighborhood_size, filename_prefix=None):
    """
    :param distance_metric: 'w' for wasserstein norm, 's' for square distance, and 'm' for max distance.
    """
    calculate_in_parallel(point_cloud, distance_metric, neighborhood_size)

    # for query in point_cloud.queries:
    #     query.topological_polysemy = results[query.identifier]
    # save_point_cloud(point_cloud, filename_prefix)
    # visualize
    # print('Topological polysemy calculated.')


def calculate_in_parallel(point_cloud, distance_metric, neighborhood_size):
    neighborhoods = point_cloud.get_neighborhoods(neighborhood_size)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_calculate)(query, neighborhood, distance_metric)
        for query, neighborhood in zip(point_cloud.queries, neighborhoods)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        query.topological_polysemy = results[query.identifier]


def _calculate(query, neighborhood, distance_metric):
    projected_neighborhood = project_to_unit_circle(neighborhood, query.point)
    zeroth_persistence_diagram = ripser.ripser(projected_neighborhood, maxdim=0)['dgms'][0]

    if distance_metric == 'w':
        topological_polysemy = compute_wasserstein_norm(zeroth_persistence_diagram)
    elif distance_metric == 's':
        topological_polysemy = compute_square_distance(zeroth_persistence_diagram)
    elif distance_metric == 'm':
        topological_polysemy = compute_max_distance(zeroth_persistence_diagram)
    else:
        topological_polysemy = None
        ValueError('Distance metric not implemented.')

    return query.identifier, topological_polysemy


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
