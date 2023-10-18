from utils.main import *


def detect(point_cloud, neighborhood_size, min_to_max_s_ratio=1, r_to_s_ratio=0.7, n_steps=1, filename_prefix=None):
    detect_in_parallel(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)
    save_point_cloud(point_cloud, filename_prefix)


def detect_in_parallel(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps):
    if None in [min_to_max_s_ratio, r_to_s_ratio]:
        annuli = point_cloud.get_annuli(neighborhood_size, n_steps)
    else:
        annuli = point_cloud.get_annuli2(neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)

    results = dict()
    for query, query_annuli in zip(point_cloud.queries, annuli):

        result = joblib.Parallel(n_jobs=-1)(
            joblib.delayed(_detect)(query, annulus, max_r, min_r)
            for annulus, max_r, min_r in query_annuli
        )
        identifier = result[0][0]
        max_r, min_r, classification = result[0][1]

        if identifier in results.keys():
            a = results[identifier]
            a[(max_r, min_r)] = classification
        else:
            results[identifier] = {(max_r, min_r): classification}

    for query in point_cloud.queries:
        query.process_classification_estimates(results[query.identifier])


def _detect(query, annulus, max_r, min_r):
    if len(annulus) != 0:
        dimension = query.intrinsic_dimension
        persistence_diagrams = ripser.ripser(annulus, maxdim=(dimension - 1))['dgms']
        classification = geometric_anomaly_detection(persistence_diagrams[-1], max_r, min_r)
        return query.identifier, (max_r, min_r, classification)


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
