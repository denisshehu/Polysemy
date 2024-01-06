import winsound

from models.point_cloud import *
from methods.topological_polysemy import *

n = 300
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec', 'fasttext', 'glove']

neighborhood_sizes = [10 * (i + 1) for i in range(20)]
min_to_max_s_ratio = 1
r_to_s_ratio = 0.1
n_steps = 1

color_bar_min = None
color_bar_max = None

for i, (embeddings_path, filename_prefix) in enumerate(zip(embeddings_paths, filename_prefixes)):
    for neighborhood_size in neighborhood_sizes:
        prefix = f'{i + 1}_{filename_prefix}_{neighborhood_size}'

        point_cloud = PointCloud()
        point_cloud.embeddings_constructor(embeddings_path, n)

        calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, filename_prefix=prefix)
        visualize_topological_polysemy(point_cloud, prefix, color_bar_min=color_bar_min, color_bar_max=color_bar_max)

winsound.Beep(500, 3000)
