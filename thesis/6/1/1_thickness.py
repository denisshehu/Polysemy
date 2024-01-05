import winsound

from models.point_cloud import *
from methods.neighborhood_thickness import *

k = 300
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec', 'fasttext', 'glove']
neighborhood_sizes = [10 * (i + 1) for i in range(20)]

for i, (embeddings_path, filename_prefix) in enumerate(zip(embeddings_paths, filename_prefixes)):

    point_cloud = PointCloud()
    point_cloud.embeddings_constructor(embeddings_path, k)

    for neighborhood_size in neighborhood_sizes:
        filename = f'{i + 1}_{filename_prefix}_{neighborhood_size}'
        calculate(point_cloud, neighborhood_size, filename)
        visualize_thickness(point_cloud, filename)

winsound.Beep(500, 3000)
