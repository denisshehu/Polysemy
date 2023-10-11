from utils.main import *


def detect(point_cloud, neighborhood_size, proportion, n_steps, filename_prefix=None):
    _detect(point_cloud, neighborhood_size, proportion, n_steps)
    # save_point_cloud(point_cloud, filename_prefix)
    # print('Classified.')


def _detect(point_cloud, neighborhood_size, proportion, n_steps):
    annuli = point_cloud.get_annuli2(neighborhood_size, proportion, n_steps)

    for index, (query, (annulus, max_r, min_r)) in enumerate(zip(point_cloud.queries, annuli)):
        dimension = query.intrinsic_dimension
        # progress = (
        #     f"Query point {i + 1} out of {len(point_cloud.queries)}: "
        #     f"Annulus {j + 1} out of {len(annulus)}."
        # )
        # print(progress, end='\r')

        if len(annulus) != 0:
            persistence_diagrams = ripser.ripser(annulus, maxdim=(dimension - 1))['dgms']
            query.classification = geometric_anomaly_detection(persistence_diagrams[-1], max_r, min_r)
            # filtered_persistence_diagrams = filter_persistence_diagrams(persistence_diagrams, True)

            # persistence_diagrams2 = ripser.ripser(annulus, maxdim=(dimension - 1), do_cocycles=True)

            # print(persistence_diagrams)
            # print()
            # print(persistence_diagrams2)

            # initial_classifications[(max_r, min_r)] = geometric_anomaly_detection(
            #     filtered_persistence_diagrams[-1], max_r, min_r)

        # print(f"{len(progress) * ' '}", end='\r')

        # query.process_initial_classifications(initial_classifications)


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
