from data_processing.data_manipulation import *
from data_processing.models.word_collection import *

fix_sco_corpus()

sc_word_collection = WordCollection(sc_paths)
sc_word_collection.extract()
sc_word_collection.save()

sco_word_collection = WordCollection(sco_paths)
sco_word_collection.extract()
sco_word_collection.save()
