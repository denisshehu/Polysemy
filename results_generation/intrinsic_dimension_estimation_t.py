from results_generation.common_t import *
from results_generation.dataframe_management import *
from results_generation.visualization_generation import *


def estimate_intrinsic_dimension(query, data, k_min, k_max, dataframe_name, outlier_parameter):
    get_raw_estimates(query, data, k_min, k_max, dataframe_name)
    generate_intrinsic_dimension_plots(dataframe_name, is_processed=False)
    remove_outliers(dataframe_name, outlier_parameter)
    generate_intrinsic_dimension_plots(dataframe_name, is_processed=True)
    compute_intrinsic_dimension(dataframe_name)


def get_raw_estimates(query, data, k_min, k_max, dataframe_name):
    word_collection = query if isinstance(query, WordCollection) else None

    if word_collection is not None:
        words = [word.value for word in word_collection.words.values()]
        n_senses = [word.n_total_senses if word_collection.used_n_total_senses else word.n_senses
                    for word in word_collection.words.values()]
        query, data = extract_query_and_data(word_collection, k_max + 2)

    for i in range(len(query)):
        q = query[i]
        for k in range(k_min, k_max + 1):
            print(f"Query point {i + 1} out of {len(query)}: [{(k - k_min + 1) * '*'}{(k_max - k) * ' '}]", end='\r')
            neighborhood = get_neighborhood(q, data, k + 2)
            estimator = skdim.id.DANCo(k=k)
            estimate = np.nan_to_num(estimator.fit_transform(neighborhood))

            word = words[i] if word_collection is not None else None
            n_senses_ = n_senses[i] if word_collection is not None else None
            point = None if word_collection is not None else query[i]

            update_intrinsic_dimension_dataframe(word=word, n_senses=n_senses_, point=point,
                                                 k=k, estimate=estimate, dataframe_name=dataframe_name)


def generate_intrinsic_dimension_plots(dataframe_name, is_processed):
    directory = after_processing_directory if is_processed else before_processing_directory
    dataframe = load_csv(os.path.join(directory, f'{dataframe_name}.csv'))
    dataframe = dataframe.dropna()

    first_column = dataframe.columns[0]
    count = 1

    for value in dataframe[first_column].unique():
        sub_dataframe = dataframe[dataframe[first_column] == value]

        if first_column == 'Word':
            n_senses = sub_dataframe['Number of senses'].iloc[0]
            figure_name = f'{value}{n_senses}_{dataframe_name}'
        else:
            figure_name = f'query{count}_{dataframe_name}'
            count += 1

        x_label = 'Number of neighbors'
        y_label = 'Intrinsic dimension estimate'
        x = sub_dataframe[x_label]
        y = sub_dataframe[y_label]
        figure_path = os.path.join(directory, figure_name)
        plot_2d(x, y, x_label, y_label, figure_path, 0, 300)


def remove_outliers(dataframe_name, k):
    dataframe = load_csv(os.path.join(before_processing_directory, f'{dataframe_name}.csv'))
    first_column = dataframe.columns[0]

    processed_estimates = []
    for value in dataframe[first_column].unique():
        sub_dataframe = dataframe[dataframe[first_column] == value]
        # estimates = np.array(sub_dataframe['Intrinsic dimension estimate']).reshape(-1, 1)
        #
        # outlier_detector = LocalOutlierFactor(n_neighbors=k)
        # results = outlier_detector.fit_predict(estimates)
        # processed_estimates += [estimates[i][0] if results[i] == 1 else np.nan for i in range(len(estimates))]

        estimates = list(sub_dataframe['Intrinsic dimension estimate'])
        estimates = [x if x <= 100 else np.nan for x in estimates]
        processed_estimates += estimates

    dataframe['Intrinsic dimension estimate'] = processed_estimates
    save_csv(dataframe, os.path.join(after_processing_directory, f'{dataframe_name}.csv'))


def compute_intrinsic_dimension(dataframe_name):
    dataframe = load_csv(os.path.join(after_processing_directory, f'{dataframe_name}.csv'))
    first_column = dataframe.columns[0]
    dataframe = dataframe.dropna()

    index = 2 if first_column == 'Word' else 1

    intrinsic_dimensions = []

    for value in dataframe[first_column].unique():
        sub_dataframe = dataframe[dataframe[first_column] == value]
        estimates = list(sub_dataframe['Intrinsic dimension estimate'])
        average = sum(estimates) / len(estimates)
        row = list(sub_dataframe.iloc[0, :index])
        row.append(average)
        intrinsic_dimensions.append(row)

    column_names = list(dataframe.columns[:index])
    column_names.append('Intrinsic dimension estimate')
    save_csv(pd.DataFrame(intrinsic_dimensions, columns=column_names),
             os.path.join(intrinsic_dimension_directory, f'intrinsic_dimension_{dataframe_name}.csv'))
