from models.point_cloud import *
from methods.topological_polysemy import *

neighborhood_size = 100
min_to_max_s_ratio = 1
r_to_s_ratio = 0.1
n_steps = 1
color_bar_min = None
color_bar_max = None

embeddings_paths = [
    ('word2vec', word2vec_embeddings_path),
    ('fasttext', fasttext_embeddings_path),
    ('glove', glove_embeddings_path)
]

for string, embeddings_path in embeddings_paths:
    prefix = f'{string}'

    point_cloud = PointCloud()
    point_cloud.embeddings_constructor(embeddings_path, 2 * neighborhood_size)

    calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, prefix)
    visualize_topological_polysemy(point_cloud, prefix, color_bar_min=color_bar_min, color_bar_max=color_bar_max)
