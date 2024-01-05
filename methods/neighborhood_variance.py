from utils.main import *


def calculate(point_cloud, neighborhood_size, n_components, filename_prefix=None):
    calculate_in_parallel(point_cloud, neighborhood_size, n_components)
    save_point_cloud(point_cloud, filename_prefix)


def calculate_in_parallel(point_cloud, neighborhood_size, n_components):
    neighborhoods = point_cloud.get_neighborhoods(neighborhood_size)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_calculate)(query, neighborhood, n_components)
        for query, neighborhood in zip(point_cloud.queries, neighborhoods)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        query.neighborhood_variance = results[query.identifier]


def _calculate(query, neighborhood, n_components):
    model = PCA(n_components=n_components)
    model.fit(neighborhood)
    variance = model.explained_variance_ratio_
    return query.identifier, variance
