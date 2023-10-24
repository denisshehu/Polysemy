import winsound

from models.point_cloud import *
from methods.neighborhood_eigenvalues import *

k = 200
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec', 'fasttext', 'glove']
neighborhood_sizes = range(10, 110, 10)

for embeddings_path, filename_prefix in zip(embeddings_paths, filename_prefixes):
    for filter_word_embeddings in [False, True]:

        point_cloud = PointCloud()
        point_cloud.embeddings_constructor(embeddings_path, k, filter_word_embeddings=filter_word_embeddings)

        for neighborhood_size in neighborhood_sizes:
            filename = f"{filename_prefix}_{'original' if not filter_word_embeddings else 'filtered'}_{neighborhood_size}"
            calculate(point_cloud, neighborhood_size, filename)
            visualize_neighborhood_eigenvalues(point_cloud, filename)

winsound.Beep(500, 3000)
