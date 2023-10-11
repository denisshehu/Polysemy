from utils.main import *


def detect(point_cloud, neighborhood_size, proportion, n_steps, filename_prefix=None):
    detect_in_parallel(point_cloud, neighborhood_size, proportion, n_steps)
    # save_point_cloud(point_cloud, filename_prefix)
    # print('Classified.')


def detect_in_parallel(point_cloud, neighborhood_size, proportion, n_steps):
    annuli = point_cloud.get_annuli2(neighborhood_size, 0.75, proportion, n_steps)

    results = list()
    for query, query_annuli in zip(point_cloud.queries, annuli):

        results_ = joblib.Parallel(n_jobs=-1)(
            joblib.delayed(_detect)(query, annulus, max_r, min_r)
            for annulus, max_r, min_r in query_annuli
        )
        results += results_

    dictionary = dict()
    for result in results:
        identifier = result[0]
        max_r, min_r, classification = result[1]
        if identifier in dictionary.keys():
            dictionary[identifier][(max_r, min_r)] = classification
        else:
            dictionary[identifier] = {(max_r, min_r): classification}

    for query in point_cloud.queries:
        query.process_initial_classifications(dictionary[query.identifier])


def _detect(query, annulus, max_r, min_r):
    if len(annulus) != 0:
        dimension = query.intrinsic_dimension
        persistence_diagrams = ripser.ripser(annulus, maxdim=(dimension - 1))['dgms']
        classification = geometric_anomaly_detection(persistence_diagrams[-1], max_r, min_r)
        return query.identifier, (max_r, min_r, classification)


def geometric_anomaly_detection(persistence_diagram, max_r, min_r):
    n_bars = 0

    threshold = max_r - min_r
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
