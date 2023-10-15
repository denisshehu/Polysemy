from utils.main import *


def detect(point_cloud, neighborhood_size, min_to_max_s_ratio=1, r_to_s_ratio=0.7, n_steps=1, filename_prefix=None):
    detect_in_parallel(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)
    save_point_cloud(point_cloud, filename_prefix)


def detect_in_parallel(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps):
    if None in [min_to_max_s_ratio, r_to_s_ratio]:
        annuli = point_cloud.get_annuli(neighborhood_size, n_steps)
    else:
        annuli = point_cloud.get_annuli2(neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_detect)(query, query_annuli)
        for query, query_annuli in zip(point_cloud.queries, annuli)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        query.process_classification_estimates(results[query.identifier])


def _detect(query, query_annuli):
    dimension = round(query.intrinsic_dimension)

    estimates = dict()
    for annulus, s, r in query_annuli:
        if len(annulus) != 0:
            persistence_diagrams = ripser.ripser(annulus, maxdim=(dimension - 1))['dgms']
            estimate = geometric_anomaly_detection(persistence_diagrams[-1], s, r)
            estimates[(s, r)] = estimate

    return query.identifier, estimates


def geometric_anomaly_detection(persistence_diagram, s, r):
    n_bars = 0

    threshold = s - r
    for feature in persistence_diagram:
        persistence = feature[1] - feature[0]
        if persistence > threshold:
            n_bars += 1

    if n_bars == 0:
        return 'boundary'
    elif n_bars == 1:
        return 'regular'
    else:
        return 'singular'
