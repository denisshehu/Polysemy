from data_processing.data_storage import *


def process_output(filename, word_collection):
    output_path = os.path.join(outputs_directory, f'{filename}output.csv')
    output = load_csv(output_path)

    n_columns = len(output.columns)
    points = [np.array2string(point) for point in output.iloc[:, :(n_columns - 2)].values]
    euclidicities = output.iloc[:, (n_columns - 2)]
    dimensions = output.iloc[:, (n_columns - 1)]

    if word_collection is None:
        results = pd.DataFrame({'Point': points, 'Dimension': dimensions, 'Euclidicity': euclidicities})
    else:
        words = [word.value for word in word_collection.words.values()]
        # attribute = 'n_total_senses' if word_collection.used_n_total_senses else 'n_senses'
        # print(word_collection.used_n_total_senses)
        # TODO: Change this!
        n_senses = [word.n_total_senses for word in word_collection.words.values()]

        results = pd.DataFrame({'Point': points, 'Word': words, 'Dimension': dimensions, 'Euclidicity': euclidicities,
                                'Number of senses': n_senses})

    results_path = os.path.join(results_subdirectory, f'{filename}results.csv')
    save_csv(results, results_path)

    summary_path = os.path.join(results_subdirectory, 'summary_results.csv')
    if os.path.exists(summary_path):
        dataframe = load_csv(summary_path)
        dataframe = pd.concat([dataframe, results])
    else:
        dataframe = results

    save_csv(dataframe, summary_path)
