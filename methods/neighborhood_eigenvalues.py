from utils.main import *


def calculate(point_cloud, neighborhood_size, filename_prefix=None):
    calculate_in_parallel(point_cloud, neighborhood_size)
    save_point_cloud(point_cloud, filename_prefix)


def calculate_in_parallel(point_cloud, neighborhood_size):
    neighborhoods = point_cloud.get_neighborhoods(neighborhood_size)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_calculate)(query, neighborhood)
        for query, neighborhood in zip(point_cloud.queries, neighborhoods)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        query.neighborhood_eigenvalues = results[query.identifier]


def _calculate(query, neighborhood):
    model = PCA()
    model.fit(neighborhood)
    eigenvalues = model.explained_variance_
    return query.identifier, eigenvalues
