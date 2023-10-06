import os.path

from utils.imports import *

# Depth 0
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Depth 1
results_directory = os.path.join(project_directory, 'results')

tardis_directory = os.path.join(os.path.dirname(project_directory), 'TARDIS2', 'tardis')
activate_path = os.path.join(os.path.dirname(tardis_directory), 'venv', 'Scripts', 'activate.bat')

normalized_gn_embeddings_path = os.path.join(project_directory, 'data', 'embeddings', 'gn_normalized.bin')
