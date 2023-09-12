from data_processing.models.word_collection import *


def update_intrinsic_dimension_dataframe(word, n_senses, point, k, estimate, dataframe_name):
    if word is not None:
        new_row = {'Word': word, 'Number of senses': n_senses, 'Number of neighbors': k,
                   'Intrinsic dimension estimate': estimate}
    else:
        new_row = {'Point': np.array2string(point), 'Number of neighbors': k, 'Intrinsic dimension estimate': estimate}

    dataframe_path = os.path.join(before_processing_directory, f'{dataframe_name}.csv')

    if os.path.exists(dataframe_path):
        dataframe = load_csv(dataframe_path)
        dataframe = pd.concat([dataframe, pd.DataFrame([new_row])])
    else:
        dataframe = pd.DataFrame([new_row])

    save_csv(dataframe, dataframe_path)
