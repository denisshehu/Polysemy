from utils.main import *


def estimate(point_cloud, neighborhood_size, maximum_dimension, min_to_max_s_ratio=None, r_to_s_ratio=None, n_steps=10,
             filename_prefix=None):
    estimate_in_parallel(point_cloud, neighborhood_size, maximum_dimension, min_to_max_s_ratio, r_to_s_ratio, n_steps)
    save_point_cloud(point_cloud, filename_prefix)


def estimate_in_parallel(point_cloud, neighborhood_size, maximum_dimension, min_to_max_s_ratio, r_to_s_ratio, n_steps):
    annuli = point_cloud.get_annuli(neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_estimate)(query, query_annuli, maximum_dimension)
        for query, query_annuli in zip(point_cloud.queries, annuli)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        estimates = results[query.identifier]
        query.intrinsic_dimension = sum(estimates) / len(estimates)


def _estimate(query, query_annuli, maximum_dimension):
    estimates = list()
    for annulus, s, r in query_annuli:
        if len(annulus) != 0:
            scaled_annulus = scale(annulus, query.point, s)
            persistence_diagrams = ripser.ripser(X=scaled_annulus, maxdim=(maximum_dimension - 1))['dgms']
            filtered_persistence_diagrams = filter_persistence_diagrams_dynamically(persistence_diagrams)
            for i in range(len(filtered_persistence_diagrams) - 1, -1, -1):
                if len(filtered_persistence_diagrams[i]) > 0:
                    estimates.append(i + 1)
                    # with open('C:\\Users\\its_d\\Desktop\\b.txt', 'a') as file:
                    #     file.write(f'{i + 1}\n')
                    #     file.write(f'{str(persistence_diagrams)}\n')
                    #     file.write(f'{str(filtered_persistence_diagrams)}\n\n')
                    break

    return query.identifier, estimates
