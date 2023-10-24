import winsound

from methods.euclidicity import *
from models.point_cloud import *

k = 300
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec', 'fasttext', 'glove']
neighborhood_sizes = [30, 50, 100, 200]  # range(10, 110, 10)

for neighborhood_size in neighborhood_sizes:
    for embeddings_path, filename_prefix in zip(embeddings_paths, filename_prefixes):

        point_cloud = PointCloud()
        point_cloud.embeddings_constructor(embeddings_path, k)

        # intrinsic_dimensions = {query.word: query.intrinsic_dimension for query in
        #                         load_yaml(
        #                             os.path.join(results_directory, f'{filename_prefix}_point_cloud.yaml')).queries}
        for query in point_cloud.queries:
            # query.intrinsic_dimension = intrinsic_dimensions[query.word]
            query.intrinsic_dimension = 3

        for min_to_max_s_ratio, r_to_s_ratio, n_steps in [(None, None, 5), (0.7, 0.7, 10)]:
            filename = f'{filename_prefix}_{neighborhood_size}_{min_to_max_s_ratio}_{r_to_s_ratio}_{n_steps}'
            calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, filename)
            visualize_euclidicity(point_cloud, filename)

winsound.Beep(500, 3000)
