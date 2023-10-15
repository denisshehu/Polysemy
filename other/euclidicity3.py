from utils.main import *


def calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, filename_prefix=None):
    calculate_in_parallel(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)
    # save_point_cloud(point_cloud, filename_prefix)
    # print('Euclidicity calculated.')


def calculate_in_parallel(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps):
    annuli = point_cloud.get_annuli2(neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_calculate)(query, query_annuli)
        for query, query_annuli in zip(point_cloud.queries, annuli)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        query.process_euclidicity_estimates(results[query.identifier])


def _calculate(query, query_annuli):
    dimension = query.intrinsic_dimension
    dimension = round(dimension)

    results = dict()
    for annulus, max_r, min_r in query_annuli:
        if len(annulus) != 0:
            diagram1 = compute_persistence_diagram(annulus, dimension, max_r, query.point)

            euclidean_annulus = sample_from_annulus(len(annulus), dimension, max_r, min_r, seed=1)
            diagram2 = compute_persistence_diagram(euclidean_annulus, dimension, max_r)

            results[(max_r, min_r)] = bottleneck_distance(diagram1, diagram2)

    return query.identifier, results


def compute_persistence_diagram(points, dimension, scaler, origin=None):
    points = scale(points, origin, scaler)
    persistence_diagrams = ripser.ripser(X=points, maxdim=(dimension - 1))['dgms']
    filtered_persistence_diagrams = filter_persistence_diagrams(persistence_diagrams)
    return np.row_stack(filtered_persistence_diagrams)
