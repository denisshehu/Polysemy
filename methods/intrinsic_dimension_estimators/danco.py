from utils.main import *


def estimate(point_cloud, min_neighborhood_size, max_neighborhood_size, filename_prefix=None):
    estimate_in_parallel(point_cloud, min_neighborhood_size, max_neighborhood_size)
    # save_point_cloud(point_cloud, filename_prefix)
    # visualize


def estimate_in_parallel(point_cloud, min_neighborhood_size, max_neighborhood_size):
    neighborhoods = point_cloud.get_neighborhoods(max_neighborhood_size + 2)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_estimate)(query, min_neighborhood_size, max_neighborhood_size, neighborhood)
        for query, neighborhood in zip(point_cloud.queries, neighborhoods)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        query.process_intrinsic_dimension_estimates(results[query.identifier])


def _estimate(query, min_neighborhood_size, max_neighborhood_size, neighborhood):
    estimates = dict()
    for neighborhood_size in range(min_neighborhood_size, max_neighborhood_size + 1):
        estimator = DANCo(k=neighborhood_size)
        estimate_ = np.nan_to_num(estimator.fit_transform(neighborhood[:(neighborhood_size + 2)]))
        estimates[neighborhood_size] = estimate_

    return query.identifier, estimates
