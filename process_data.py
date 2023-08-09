from data_processing.data_manipulation import *
from data_processing.models.word_collection import *

fix_sco_corpus()

normalize_embeddings(gn_embeddings_path, normalized_gn_embeddings_path)

sc_word_collection = WordCollection(sc_corpus_path, gn_embeddings_path, sc_senses_path, sc_word_collection_path)

normalized_sc_word_collection = WordCollection(sc_corpus_path, normalized_gn_embeddings_path, sc_senses_path,
                                               normalized_sc_word_collection_path)

sco_word_collection = WordCollection(fixed_sco_corpus_path, gn_embeddings_path, sco_senses_path,
                                     sco_word_collection_path)

normalized_sco_word_collection = WordCollection(fixed_sco_corpus_path, normalized_gn_embeddings_path, sco_senses_path,
                                                normalized_sco_word_collection_path)
