import winsound

from results_processing.main_t import *

sc_word_collection = load_yaml(normalized_sc_word_collection_path)
words = sc_word_collection.get_monosemes_and_polysemes(n=100, use_n_total_senses=True)

n_neighbors_values = [(i + 1) for i in range(90)]
filename_prefix = '200td_danco'

max_dimension = 10

for n_neighbors in n_neighbors_values:
    get_results(query=words, n_neighbors=n_neighbors, max_dimension=max_dimension, seed=1,
                filename_prefix=filename_prefix, keep_terminal_open=False)

winsound.Beep(500, 3000)
