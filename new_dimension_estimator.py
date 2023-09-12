import winsound

from results_generation.intrinsic_dimension_estimation_t import *

word_collection = load_yaml(normalized_sc_word_collection_path)
query = word_collection.get_monosemes_and_polysemes(n=100, use_n_total_senses=True)

estimate_intrinsic_dimension(query, None, 30, 45, '200t', 2)

winsound.Beep(500, 3000)
