from utils.main import *


def estimate_intrinsic_dimension(point_cloud, min_neighborhood_size, max_neighborhood_size, filename_prefix=None):
    get_initial_estimates(point_cloud, min_neighborhood_size, max_neighborhood_size)
    point_cloud.process_intrinsic_dimension_estimates()
    save_point_cloud(point_cloud, filename_prefix)
    # visualize


def get_initial_estimates(point_cloud, min_neighborhood_size, max_neighborhood_size):
    for neighborhood_size in range(min_neighborhood_size, max_neighborhood_size + 1):
        neighborhoods = point_cloud.get_neighborhoods(neighborhood_size + 2)

        for index, (query, neighborhood) in enumerate(zip(point_cloud.queries, neighborhoods)):
            progress = (
                f'Neighborhood size = {neighborhood_size} ({neighborhood_size - min_neighborhood_size + 1}/'
                f'{max_neighborhood_size - min_neighborhood_size + 1}): '
                f'Query point {index + 1} out of {len(point_cloud.queries)}.'
            )
            print(progress, end='\r')

            estimator = DANCo(k=neighborhood_size)
            estimate = np.nan_to_num(estimator.fit_transform(neighborhood))
            query.add_intrinsic_dimension_estimate(neighborhood_size, estimate)

            print(f"{len(progress) * ' '}", end='\r')
    print('Intrinsic dimension estimated.')
