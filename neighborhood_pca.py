import winsound

from models.point_cloud import *
from methods.neighborhood_pca import *

k = 200
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec', 'fasttext', 'glove']
# neighborhood_sizes = range(10, 110, 10)

for embeddings_path, filename_prefix in zip(embeddings_paths, filename_prefixes):

    point_cloud = PointCloud()
    point_cloud.embeddings_constructor(embeddings_path, k)

    # for neighborhood_size in neighborhood_sizes:
    neighborhood_size = 100
    filename = f'{filename_prefix}_{neighborhood_size}'
    calculate(point_cloud, neighborhood_size, filename)

winsound.Beep(500, 3000)
