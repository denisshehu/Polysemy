from utils.main import *


def calculate(point_cloud, neighborhood_size, filename_prefix=None):
    calculate_in_parallel(point_cloud, neighborhood_size)
    save_point_cloud(point_cloud, filename_prefix)


def calculate_in_parallel(point_cloud, neighborhood_size):
    neighborhoods = point_cloud.get_neighborhoods(neighborhood_size)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_calculate)(query, neighborhood)
        for query, neighborhood in zip(point_cloud.queries, neighborhoods)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        original_neighborhood_thickness, translated_neighborhood_thickness = results[query.identifier]
        query.original_neighborhood_thickness = original_neighborhood_thickness
        query.translated_neighborhood_thickness = translated_neighborhood_thickness


def _calculate(query, neighborhood):
    original_neighborhood_thickness = get_neighborhood_thickness(neighborhood)
    translated_neighborhood_thickness = get_neighborhood_thickness(translate(neighborhood, query.point))

    return query.identifier, (original_neighborhood_thickness, translated_neighborhood_thickness)


def get_neighborhood_thickness(neighborhood):
    neighborhood_thickness = 0
    for i in range(len(neighborhood)):
        for j in range(i + 1, len(neighborhood)):
            point1 = neighborhood[i]
            point2 = neighborhood[j]

            cosine_similarity = np.dot(point1, point2) / (np.linalg.norm(point1) * np.linalg.norm(point2))
            angle_in_degrees = math.degrees(math.acos(cosine_similarity))
            neighborhood_thickness = max(neighborhood_thickness, angle_in_degrees)

    return neighborhood_thickness
