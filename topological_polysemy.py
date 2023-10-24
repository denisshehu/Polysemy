import winsound

from models.point_cloud import *
from methods.topological_polysemy import *

k = 300
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec', 'fasttext', 'glove']
neighborhood_sizes = [50, 100, 200]

for embeddings_path, filename_prefix in zip(embeddings_paths, filename_prefixes):

    point_cloud = PointCloud()
    point_cloud.embeddings_constructor(embeddings_path, k)

    for neighborhood_size in neighborhood_sizes:
        for min_to_max_s_ratio, r_to_s_ratio, n_steps in [(1, 0, 1), (1, 0.7, 1), (0.7, 0.7, 10)]:
            filename = f'{filename_prefix}_{neighborhood_size}_{min_to_max_s_ratio}_{r_to_s_ratio}_{n_steps}'
            calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, filename)
            visualize_topological_polysemy(point_cloud, filename)

winsound.Beep(500, 3000)
