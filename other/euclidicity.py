import time

import numpy as np
from gph import ripser_parallel
from gudhi.bottleneck import bottleneck_distance

from methods.common_functions import save_point_cloud, scale_annulus, filter_persistence_diagrams
from sample_generation import sample_from_annulus2


def calculate_euclidicity(point_cloud, neighborhood_size, n_steps, filename_prefix=None):
    calculate(point_cloud, neighborhood_size, n_steps)
    save_point_cloud(point_cloud, filename_prefix)
    print('Euclidicity calculated.')


def calculate(point_cloud, neighborhood_size, n_steps):
    annuli = point_cloud.get_annuli(neighborhood_size, n_steps)

    for i, (query, query_annuli) in enumerate(zip(point_cloud.queries, annuli)):
        dimension = query.intrinsic_dimension

        euclidicity_estimates = dict()
        for j, (annulus, max_r, min_r) in enumerate(query_annuli):
            # progress = (
            #     f"Query point {i + 1} out of {len(point_cloud.queries)}: "
            #     f"Annulus {j + 1} out of {len(query_annuli)}."
            # )
            # print(progress, end='\r')

            if len(annulus) != 0:
                print(f'Ready for n = {len(annulus)}, d = {dimension}, s = {max_r}, r = {min_r}.')
                print('Annulus:')
                diagram1 = compute_persistence_diagram(annulus, max_r, dimension, query.point)

                print('Euclidean annulus:')
                start = time.time()
                euclidean_annulus = sample_from_annulus2(len(annulus), dimension, max_r, min_r, seed=None)
                end = time.time()
                print(f'Euclidean annulus sampled in {end - start} seconds.')

                diagram2 = compute_persistence_diagram(euclidean_annulus, max_r, dimension)

                euclidicity_estimates[(max_r, min_r)] = bottleneck_distance(diagram1, diagram2)
                print('')

            # print(f"{len(progress) * ' '}", end='\r')

        query.process_euclidicity_estimates(euclidicity_estimates)


def compute_persistence_diagram(annulus, scaler, dimension, point=None):
    scaled_annulus = scale_annulus(annulus, scaler, point)
    start = time.time()
    persistence_diagrams = ripser_parallel(scaled_annulus, maxdim=(dimension - 1), collapse_edges=True)['dgms']
    end = time.time()
    print(f'Persistence diagram computed in {end - start} seconds.')
    filtered_persistence_diagrams = filter_persistence_diagrams(persistence_diagrams)
    return np.row_stack(filtered_persistence_diagrams)
