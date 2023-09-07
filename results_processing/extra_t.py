import matplotlib.pyplot as plt

from data_processing.data_storage import *


def update_dataframe(filename):
    parameters = filename.split('_')
    e = parameters[0]
    d = parameters[1]
    n = parameters[2][1:]
    k = parameters[3][1:]
    max_d = parameters[4][1:]

    results_path = os.path.join(results_subdirectory, f'{filename}results.csv')
    results = load_csv(results_path)

    dimension = results['Dimension'][0]

    # new_row = {'Intrinsic dimension': d, 'Size of data': n, 'Number of neighbors': k, 'Estimator': e,
    #            'Maximum dimension': max_d, 'Estimate': dimension}

    new_row = {'Intrinsic dimension': d, 'Size of data': n, 'Number of neighbors': k, 'Estimator': e,
               'Estimate': dimension}

    dataframe_path = os.path.join(results_directory, f'{e}.csv')

    if os.path.exists(dataframe_path):
        dataframe = load_csv(dataframe_path)
        dataframe = pd.concat([dataframe, pd.DataFrame([new_row])])
        save_csv(dataframe, dataframe_path)
    else:
        dataframe = pd.DataFrame([new_row])
        save_csv(dataframe, dataframe_path)


def update_dataframe_words(filename):
    parameters = filename.split('_')
    k = parameters[3][1:]
    max_d = parameters[4][1:]

    results_path = os.path.join(results_subdirectory, f'{filename}results.csv')
    results = load_csv(results_path)

    words = results['Word']
    senses = results['Number of senses']
    dimensions = results['Dimension']

    new_rows = [{'Word': words[i], 'Number of senses': senses[i], 'Number of neighbors': k,
                 'Estimate': dimensions[i]} for i in range(len(words))]

    dataframe_path = os.path.join(results_directory, 'danco.csv')

    if os.path.exists(dataframe_path):
        dataframe = load_csv(dataframe_path)
        dataframe = pd.concat([dataframe, pd.DataFrame(new_rows)])
        save_csv(dataframe, dataframe_path)
    else:
        dataframe = pd.DataFrame(new_rows)
        save_csv(dataframe, dataframe_path)


def plot_dataframe(dataframe_filename):
    dataframe_path = os.path.join(results_directory, dataframe_filename)
    dataframe = load_csv(dataframe_path)

    dimensions = dataframe['Intrinsic dimension'].unique()

    for dimension in dimensions:
        dataframe_d = dataframe[dataframe['Intrinsic dimension'] == dimension]

        n_neighbors = dataframe_d['Number of neighbors']
        estimates = dataframe_d['Estimate']

        plot(dimension, n_neighbors, estimates)


def plot(dimension, n_neighbors, estimates):
    plt.figure(figsize=(15, 5))
    plt.plot(n_neighbors, estimates, marker='o', linestyle='-', color='b')
    # plt.axhline(y=(dimension + 0.5), color='red', linestyle='--')
    plt.axhline(y=dimension, color='red', linestyle='--')
    # plt.axhline(y=(dimension - 0.5), color='red', linestyle='--')
    plt.ylim(0)
    plt.xlabel('Number of neighbors')
    plt.ylabel('Dimension estimate')
    plt.savefig(os.path.join(results_directory, f'{dimension}.png'), dpi=300)
    plt.close()


def plot_dataframe_words(dataframe_filename):
    dataframe_path = os.path.join(results_directory, dataframe_filename)
    dataframe = load_csv(dataframe_path)

    words = dataframe['Word'].unique()

    for word in words:
        dataframe_w = dataframe[dataframe['Word'] == word]

        n_neighbors = dataframe_w['Number of neighbors']
        estimates = dataframe_w['Estimate']
        n_senses = dataframe_w['Number of senses'].unique()[0]

        plot_words(word, n_neighbors, estimates, n_senses)


def plot_words(word, n_neighbors, estimates, n_senses):
    plt.figure(figsize=(15, 5))
    plt.plot(n_neighbors, estimates, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of neighbors')
    plt.ylabel('Dimension estimate')
    plt.savefig(os.path.join(results_directory, f'{word}_senses{n_senses}.png'), dpi=300)
    plt.close()


def update_dataframe_e(filename):
    parameters = filename.split('_')
    type = parameters[0]
    D = parameters[1][1:]
    n = parameters[2][1:]
    k = parameters[3][1:]
    d = parameters[4][1:]

    results_path = os.path.join(results_subdirectory, f'{filename}results.csv')
    results = load_csv(results_path)

    euclidicity = results['Euclidicity'][0]

    new_row = {'Dimension of data': D, 'Intrinsic dimension': d, 'Size of data': n, 'Number of neighbors': k,
               'Type': type, 'Euclidicity': euclidicity}

    dataframe_path = os.path.join(results_directory, f'euclidicities.csv')

    if os.path.exists(dataframe_path):
        dataframe = load_csv(dataframe_path)
        dataframe = pd.concat([dataframe, pd.DataFrame([new_row])])
        save_csv(dataframe, dataframe_path)
    else:
        dataframe = pd.DataFrame([new_row])
        save_csv(dataframe, dataframe_path)


def plot_euclidicities(dataframe_filename):
    dataframe_path = os.path.join(results_directory, dataframe_filename)
    dataframe = load_csv(dataframe_path)

    dimension_300 = dataframe[dataframe['Dimension of data'] == 300]
    dimension_not_300 = dataframe[dataframe['Dimension of data'] != 300]

    regular_300 = dimension_300[dimension_300['Type'] == 'regular']
    singularity_300 = dimension_300[dimension_300['Type'] == 'singularity']
    regular_not_300 = dimension_not_300[dimension_not_300['Type'] == 'regular']
    singularity_not_300 = dimension_not_300[dimension_not_300['Type'] == 'singularity']

    plt.figure(figsize=(15, 5))
    plt.plot(regular_not_300['Intrinsic dimension'], regular_not_300['Euclidicity'], marker='o', linestyle='-',
             color='b', label='Regular')
    plt.plot(singularity_not_300['Intrinsic dimension'], singularity_not_300['Euclidicity'], marker='o',
             linestyle='-', color='orange', label='Singularity')
    plt.xlabel('Intrinsic dimension')
    plt.ylabel('Euclidicity')
    plt.legend()
    plt.savefig(os.path.join(results_directory, 'not_300.png'), dpi=300)
    plt.close()

    plt.figure(figsize=(15, 5))
    plt.plot(regular_300['Intrinsic dimension'], regular_300['Euclidicity'], marker='o', linestyle='-',
             color='b', label='Regular')
    plt.plot(singularity_300['Intrinsic dimension'], singularity_300['Euclidicity'], marker='o',
             linestyle='-', color='orange', label='Singularity')
    plt.xlabel('Intrinsic dimension')
    plt.ylabel('Euclidicity')
    plt.legend()
    plt.savefig(os.path.join(results_directory, '300.png'), dpi=300)
    plt.close()


def plot_euclidicities_1(dataframe_filename):
    dataframe_path = os.path.join(results_directory, dataframe_filename)
    dataframe = load_csv(dataframe_path)

    regular = dataframe[dataframe['Type'] == 'regular']
    singularity = dataframe[dataframe['Type'] == 'singularity']

    dimensions = dataframe['Intrinsic dimension'].unique()

    for dimension in dimensions:
        plot_1(regular[regular['Intrinsic dimension'] == dimension],
               singularity[singularity['Intrinsic dimension'] == dimension], dimension)


def plot_1(regular, singularity, dimension):
    plt.figure(figsize=(15, 5))
    plt.plot(regular['Number of neighbors'], regular['Euclidicity'], marker='o', linestyle='-',
             color='b', label='Regular')
    plt.plot(singularity['Number of neighbors'], singularity['Euclidicity'], marker='o',
             linestyle='-', color='orange', label='Singularity')
    plt.xlabel('Number of neighbors')
    plt.ylabel('Euclidicity')
    plt.legend()
    plt.savefig(os.path.join(results_directory, f'{dimension}.png'), dpi=300)
    plt.close()


def update_dataframe_e1(filename):
    parameters = filename.split('_')
    type = parameters[0]
    real_d = parameters[1][5:]
    k = parameters[3][1:]
    d = parameters[4][1:]

    results_path = os.path.join(results_subdirectory, f'{filename}results.csv')
    results = load_csv(results_path)

    euclidicity = results['Euclidicity'][0]

    new_row = {'Real intrinsic dimension': real_d, 'Estimated intrinsic dimension': d, 'Number of neighbors': k,
               'Type': type, 'Euclidicity': euclidicity}

    dataframe_path = os.path.join(results_directory, f'euclidicities.csv')

    if os.path.exists(dataframe_path):
        dataframe = load_csv(dataframe_path)
        dataframe = pd.concat([dataframe, pd.DataFrame([new_row])])
        save_csv(dataframe, dataframe_path)
    else:
        dataframe = pd.DataFrame([new_row])
        save_csv(dataframe, dataframe_path)


def plot_euclidicities_2(dataframe_filename):
    dataframe_path = os.path.join(results_directory, dataframe_filename)
    dataframe = load_csv(dataframe_path)

    regular = dataframe[dataframe['Type'] == 'regular']
    singularity = dataframe[dataframe['Type'] == 'singularity']

    real_dimensions = dataframe['Real intrinsic dimension'].unique()

    for real_dimension in real_dimensions:
        plot_2(regular[regular['Real intrinsic dimension'] == real_dimension],
               singularity[singularity['Real intrinsic dimension'] == real_dimension], real_dimension)


def plot_2(regular, singularity, real_dimension):
    plt.figure(figsize=(15, 5))
    plt.plot(regular['Estimated intrinsic dimension'], regular['Euclidicity'], marker='o', linestyle='-',
             color='b', label='Regular')
    plt.axhline(y=regular[regular['Estimated intrinsic dimension'] == real_dimension]['Euclidicity'].iloc[0], color='b',
                linestyle='--')
    plt.plot(singularity['Estimated intrinsic dimension'], singularity['Euclidicity'], marker='o',
             linestyle='-', color='orange', label='Singularity')
    plt.axhline(y=singularity[singularity['Estimated intrinsic dimension'] == real_dimension]['Euclidicity'].iloc[0],
                color='orange', linestyle='--')
    plt.xlabel('Estimated intrinsic dimension')
    plt.ylabel('Euclidicity')
    plt.legend()
    plt.savefig(os.path.join(results_directory, f'{real_dimension}.png'), dpi=300)
    plt.close()
