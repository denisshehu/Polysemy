import os

# nltk.download('wordnet')

word2vec_model_name = 'word2vec-google-news-300'
fasttext_model_name = 'fasttext-wiki-news-subwords-300'

# Depth 0
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Depth 1
embeddings_directory = os.path.join(project_directory, '../OLD/embeddings')
results_directory = os.path.join(project_directory, '../results')

# Depth 2
word2vec_path = os.path.join(embeddings_directory, 'gn_normalized.bin')
fasttext_path = os.path.join(embeddings_directory, 'crawl-300d-2M-subword.bin')

tardis_directory = os.path.join(os.path.dirname(project_directory), 'TARDIS2', 'tardis')
activate_path = os.path.join(os.path.dirname(tardis_directory), '../venv', 'Scripts', 'activate.bat')
