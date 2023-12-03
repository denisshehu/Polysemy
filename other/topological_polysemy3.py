from utils.main import *


def calculate(point_cloud, neighborhood_size, filename_prefix=None):
    calculate_in_parallel(point_cloud, neighborhood_size)
    # save_point_cloud(point_cloud, filename_prefix)
    # visualize


def calculate_in_parallel(point_cloud, neighborhood_size):
    neighborhoods = point_cloud.get_neighborhoods(neighborhood_size)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_calculate)(query, neighborhood)
        for query, neighborhood in zip(point_cloud.queries, neighborhoods)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        query.topological_polysemy = results[query.identifier]


def _calculate(query, neighborhood):
    projected_neighborhood = project_to_unit_sphere(neighborhood, query.point)
    zeroth_persistence_diagram = ripser.ripser(projected_neighborhood, maxdim=0)['dgms'][0]
    topological_polysemy = wasserstein_distance(X=zeroth_persistence_diagram, Y=np.array([[0, np.inf]]))
    return query.identifier, topological_polysemy
