from results_generation.results_visualization_t import *


def extra_plots(dataframe_name, word_collection):
    words = [word for word in word_collection.words.values()]
    # values = [word.value for word in words]
    n_senses = [word.n_total_senses if word_collection.used_n_total_senses else word.n_senses for word in words]
    counts = [word.count for word in words]
    pos_counts = [len(word.pos_counts) for word in words]

    dataframe = load_csv(os.path.join(intrinsic_dimension_directory, f'intrinsic_dimension_{dataframe_name}.csv'))

    intrinsic_dimensions = list(dataframe['Intrinsic dimension estimate'])

    plot_2d(n_senses, intrinsic_dimensions, 'Number of senses', 'Intrinsic dimension estimate',
            os.path.join(intrinsic_dimension_directory, f'extra_senses.png'), n_senses)

    plot_2d(counts, intrinsic_dimensions, 'Word count', 'Intrinsic dimension estimate',
            os.path.join(intrinsic_dimension_directory, f'extra_count.png'), n_senses)

    plot_2d(pos_counts, intrinsic_dimensions, 'POS count', 'Intrinsic dimension estimate',
            os.path.join(intrinsic_dimension_directory, f'extra_pos.png'), n_senses)
