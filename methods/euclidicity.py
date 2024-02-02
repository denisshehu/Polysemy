from utils.main import *


def calculate(point_cloud, neighborhood_size, min_to_max_s_ratio=None, r_to_s_ratio=None, n_steps=10,
              perform_scaling=True, filtering=None, filename_prefix=None):
    calculate_in_parallel(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, perform_scaling,
                          filtering)
    save_point_cloud(point_cloud, filename_prefix)


def calculate_in_parallel(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, perform_scaling,
                          filtering):
    annuli = point_cloud.get_annuli(neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_calculate)(query, query_annuli, perform_scaling, filtering)
        for query, query_annuli in zip(point_cloud.queries, annuli)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        query.process_euclidicity_estimates(results[query.identifier])


def _calculate(query, query_annuli, perform_scaling, filtering):
    dimension = round(query.intrinsic_dimension)

    estimates = dict()
    for annulus, s, r in query_annuli:
        if len(annulus) != 0:
            scaler = s if perform_scaling else None
            diagram1 = compute_persistence_diagram(annulus, dimension, scaler, filtering, query.point)

            euclidean_annulus = sample_from_annulus(len(annulus), dimension, s, r, seed=1,
                                                    ambient_dimension=np.shape(query.point)[0])
            diagram2 = compute_persistence_diagram(euclidean_annulus, dimension, scaler, filtering)

            estimate = bottleneck_distance(diagram1, diagram2)
            estimates[(s, r)] = estimate

    return query.identifier, estimates


def compute_persistence_diagram(points, dimension, scaler, filtering, origin=None):
    if scaler is not None:
        points = scale(points, origin, scaler)
    persistence_diagrams = ripser.ripser(X=points, maxdim=(dimension - 1))['dgms']
    if isinstance(filtering, str):
        persistence_diagrams = filter_persistence_diagrams_dynamically(persistence_diagrams)
    elif isinstance(filtering, float):
        persistence_diagrams = filter_persistence_diagrams_statically(persistence_diagrams, filtering)
    return np.row_stack(persistence_diagrams)
