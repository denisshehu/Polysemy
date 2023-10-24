from utils.storage import *


def tabulate_neighborhood_thickness(point_cloud, table_name_prefix):
    queries = point_cloud.queries
    identifiers = [query.identifier for query in queries]
    words = [query.word for query in queries]
    word_types = [query.word_type for query in queries]
    original_neighborhood_thickness = [query.original_neighborhood_thickness for query in queries]
    translated_neighborhood_thickness = [query.translated_neighborhood_thickness for query in queries]

    are_words_none = None in words
    if are_words_none:
        data = np.array([identifiers, original_neighborhood_thickness, translated_neighborhood_thickness]).T
        column_names = ['ID', 'Original', 'Translated']
    else:
        data = np.array([words, word_types, original_neighborhood_thickness, translated_neighborhood_thickness]).T
        column_names = ['Word', 'Type', 'Original', 'Translated']

    dataframe = pd.DataFrame(data, columns=column_names)
    save_csv(dataframe, os.path.join(results_directory, f'{table_name_prefix}_neighborhood_thickness.csv'))
