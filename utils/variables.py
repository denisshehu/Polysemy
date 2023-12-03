from utils.imports import *

# Depth 0
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Depth 1
embeddings_directory = os.path.join(project_directory, 'embeddings')
evaluation_directory = os.path.join(project_directory, 'evaluation')
results_directory = os.path.join(project_directory, 'results')
utils_directory = os.path.join(project_directory, 'utils')

# Depth 2
fasttext_embeddings_path = os.path.join(embeddings_directory, 'fasttext.bin')
glove_embeddings_path = os.path.join(embeddings_directory, 'glove.txt')
word2vec_embeddings_path = os.path.join(embeddings_directory, 'word2vec.bin')

ws_path = os.path.join(evaluation_directory, 'ws.txt')
ws_similarity_path = os.path.join(evaluation_directory, 'ws_similarity.txt')
ws_relatedness_path = os.path.join(evaluation_directory, 'ws_relatedness.txt')

words_path = os.path.join(utils_directory, 'words.csv')

# Other
tardis_directory = os.path.join(os.path.dirname(project_directory), 'TARDIS2', 'tardis')
activate_path = os.path.join(os.path.dirname(tardis_directory), 'venv', 'Scripts', 'activate.bat')

normalized_gn_embeddings_path = os.path.join(project_directory, 'data', 'embeddings', 'gn_normalized.bin')
semcor = os.path.join(project_directory, 'data', 'word_collections', 'sc_normalized.yaml')
