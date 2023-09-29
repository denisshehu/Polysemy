from utils.imports import *

# Depth 0
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Depth 1
results_directory = os.path.join(project_directory, 'results')

normalized_gn_embeddings_path = os.path.join(project_directory, 'data', 'embeddings', 'gn_normalized.bin')
