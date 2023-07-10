import os
import numpy as np
import xml.etree.ElementTree as ElementTree
from gensim.models import KeyedVectors
import yaml

# Depth 0
project_directory = os.path.dirname(os.path.abspath(__file__))

# Depth 1
data_directory = os.path.join(project_directory, 'data')
results_directory = os.path.join(project_directory, 'results')

# Depth 2 (data)
corpora_directory = os.path.join(data_directory, 'corpora')
embeddings_directory = os.path.join(data_directory, 'embeddings')
senses_directory = os.path.join(data_directory, 'senses')
word_collections_directory = os.path.join(data_directory, 'word_collections')

# Depth 2 (results)
inputs_directory = os.path.join(results_directory, 'inputs')
query_points_directory = os.path.join(results_directory, 'query_points')
outputs_directory = os.path.join(results_directory, 'outputs')

# Depth 3 (corpora)
sc_corpus_path = os.path.join(corpora_directory, 'sc.xml')
sco_corpus_path = os.path.join(corpora_directory, 'sco.xml')
fixed_sco_corpus_path = os.path.join(corpora_directory, 'sco_fixed.xml')

# Depth 3 (embeddings)
gn_embeddings_path = os.path.join(embeddings_directory, 'gn.bin')

# Depth 3 (senses)
sc_senses_path = os.path.join(senses_directory, 'sc.txt')
sco_senses_path = os.path.join(senses_directory, 'sco.txt')

# Depth 3 (word_collections)
sc_word_collection_path = os.path.join(word_collections_directory, 'sc.yaml')
sco_word_collection_path = os.path.join(word_collections_directory, 'sco.yaml')

sc_paths = (sc_corpus_path, gn_embeddings_path, sc_senses_path, sc_word_collection_path)
sco_paths = (fixed_sco_corpus_path, gn_embeddings_path, sco_senses_path, sco_word_collection_path)
