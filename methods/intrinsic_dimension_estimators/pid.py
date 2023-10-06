from utils.main import *


def estimate(point_cloud, neighborhood_size, maximum_dimension, n_steps, filename_prefix=None):
    estimate_in_parallel(point_cloud, neighborhood_size, maximum_dimension, n_steps)


def estimate_in_parallel(point_cloud, neighborhood_size, maximum_dimension, n_steps):
    annuli = point_cloud.get_annuli(neighborhood_size, n_steps)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_estimate)(query, query_annuli, maximum_dimension)
        for query, query_annuli in zip(point_cloud.queries, annuli)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        estimates = results[query.identifier]
        query.intrinsic_dimension = sum(estimates) / len(estimates)


def _estimate(query, query_annuli, maximum_dimension):
    estimates = []
    for annulus, _, _ in query_annuli:
        if len(annulus) != 0:
            persistence_diagrams = ripser.ripser(X=annulus, maxdim=(maximum_dimension - 1))['dgms']
            persistence_diagrams = filter_persistence_diagrams(persistence_diagrams)
            estimates.append(len(persistence_diagrams))
    return query.identifier, estimates
