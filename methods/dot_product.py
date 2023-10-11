from utils.main import *


def calculate(point_cloud, neighborhood_size, filename_prefix=None):
    calculate_in_parallel(point_cloud, neighborhood_size, filename_prefix)
    # save_point_cloud(point_cloud, filename_prefix)
    # visualize


def calculate_in_parallel(point_cloud, neighborhood_size, filename_prefix):
    neighborhoods = point_cloud.get_neighborhoods(neighborhood_size)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_calculate)(query, neighborhood)
        for query, neighborhood in zip(point_cloud.queries, neighborhoods)
    )
    # results = {key: value for key, value in results}

    if point_cloud.queries[0].word is None:
        dataframe = pd.DataFrame(results, columns=['ID', 'Original', 'Translated'])
    else:
        dataframe = pd.DataFrame(results, columns=['Word', 'Type', 'Original', 'Translated'])
    save_csv(dataframe, os.path.join(results_directory, f'{filename_prefix}.csv'))


def _calculate(query, neighborhood):
    original = a(neighborhood)
    translated = a(translate(neighborhood, query.point))

    if query.word is None:
        return query.identifier, original, translated
    else:
        return query.word, query._word_type, original, translated


def a(neighborhood):
    max_angle_in_degrees = 0
    for i in range(len(neighborhood)):
        for j in range(i + 1, len(neighborhood)):
            point1 = neighborhood[i]
            point2 = neighborhood[j]
            cosine_similarity = np.dot(point1, point2) / (np.linalg.norm(point1) * np.linalg.norm(point2))
            angle_in_degrees = math.degrees(math.acos(cosine_similarity))
            max_angle_in_degrees = max(max_angle_in_degrees, angle_in_degrees)
    return max_angle_in_degrees
