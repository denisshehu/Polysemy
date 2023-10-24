import winsound

from models.point_cloud import *
from methods.intrinsic_dimension_estimators.danco import *
from utils.visualization_generation import *

k = 200
min_neighborhood_size = 0
max_neighborhood_size = 2
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec']#, 'fasttext', 'glove']

for embeddings_path, filename_prefix in zip(embeddings_paths, filename_prefixes):
    point_cloud = PointCloud()
    point_cloud.embeddings_constructor(embeddings_path, k, filter_word_embeddings=True)

    a = f'{filename_prefix}'
    estimate(point_cloud, min_neighborhood_size, max_neighborhood_size, a)
    visualize_dimension(point_cloud, a)

winsound.Beep(500, 3000)
