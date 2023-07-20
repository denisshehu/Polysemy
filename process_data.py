from data_processing.data_manipulation import *
from data_processing.models.word_collection import *

fix_sco_corpus()

normalize_embeddings(gn_embeddings_path, normalized_gn_embeddings_path)

sc_word_collection = WordCollection(sc_paths)
sc_word_collection.extract()
sc_word_collection.save()

normalized_sc_word_collection = WordCollection(normalized_sc_paths)
normalized_sc_word_collection.extract()
normalized_sc_word_collection.save()

sco_word_collection = WordCollection(sco_paths)
sco_word_collection.extract()
sco_word_collection.save()

normalized_sco_word_collection = WordCollection(normalized_sco_paths)
normalized_sco_word_collection.extract()
normalized_sco_word_collection.save()
