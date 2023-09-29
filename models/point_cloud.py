from utils.main import *
from models.query import Query


class PointCloud:

    def __init__(self):
        self._points = None
        self._tree = None
        self._queries = None

    def random_constructor(self, points, n_queries):
        self._points = points
        self._tree = KDTree(points)

        n_points = points.shape[0]
        indices = np.random.choice(a=n_points, size=n_queries, replace=False)
        query_points = points[indices]
        queries = [Query(point) for point in query_points]

        self._queries = queries

    def non_random_constructor(self, points, query_points):
        self._points = points
        self._tree = KDTree(points)

        queries = [Query(point) for point in query_points] if len(query_points.shape) != 1 else [Query(query_points)]

        self._queries = queries

    def embeddings_constructor(self, model_name, query_keys, neighborhood_size):
        embeddings = gensim.downloader.load(model_name)
        embeddings.unit_normalize_all()

        query_points = [embeddings[key] for key in query_keys]
        queries = [Query(point, key) for point, key in zip(query_points, query_keys)]

        point_keys = set()
        for point in query_points:
            most_similar = embeddings.similar_by_vector(vector=point, topn=(neighborhood_size + 1))
            point_keys.update([key for key, similarity in most_similar])
        points = np.array([embeddings[key] for key in point_keys])

        self._points = points
        self._tree = KDTree(points)
        self._queries = queries

    # def fasttext_constructor(self, embeddings_path, query_keys, neighborhood_size):
    #     embeddings = FastText.load_fasttext_format(embeddings_path).wv
    #     embeddings.unit_normalize_all()
    #
    #     query_points = [embeddings[key] for key in query_keys]
    #     queries = [Query(point, key) for point, key in zip(query_points, query_keys)]
    #
    #     point_keys = set()
    #     for point in query_points:
    #         most_similar = embeddings.similar_by_vector(vector=point, topn=(neighborhood_size + 1))
    #         point_keys.update([key for key, similarity in most_similar])
    #     points = np.array([embeddings[key] for key in point_keys])
    #
    #     self._points = points
    #     self._tree = KDTree(points)
    #     self._queries = queries

    @property
    def points(self):
        return self._points

    # @property
    # def tree(self):
    #     return self._tree

    @property
    def queries(self):
        return self._queries

    def get_query_points(self):
        query_points = np.array([query.point for query in self._queries])
        return query_points

    def _get_distances_and_indices(self, neighborhood_size):
        query_points = self.get_query_points()
        distances, indices = self._tree.query(X=query_points, k=(neighborhood_size + 1))

        indices = np.array([
            indices[i][1:] if distances[i][0] == 0 else indices[i][:-1] for i in range(len(indices))
        ])
        distances = np.array([
            distances[i][1:] if distances[i][0] == 0 else distances[i][:-1] for i in range(len(distances))
        ])
        return distances, indices

    def get_neighborhoods(self, neighborhood_size):
        distances, indices = self._get_distances_and_indices(neighborhood_size)

        neighborhoods = self._points[indices]
        return neighborhoods

    def _get_annulus(self, point, max_r, min_r):
        large_ball_indices = self._tree.query_radius(X=point.reshape(1, -1), r=max_r)[0]
        small_ball_indices = self._tree.query_radius(X=point.reshape(1, -1), r=min_r)[0]
        annulus_indices = np.setdiff1d(ar1=large_ball_indices, ar2=small_ball_indices)

        annulus = (self._points[annulus_indices], max_r, min_r)
        return annulus

    def get_annuli(self, neighborhood_size, n_steps):
        distances, indices = self._get_distances_and_indices(neighborhood_size)
        radii = [[d[0], d[neighborhood_size // 3 - 1], d[-1]] for d in distances]

        annuli = list()
        for point, point_radii in zip(self.get_query_points(), radii):
            point_annuli = list()

            for max_r in np.linspace(start=point_radii[1], stop=point_radii[2], num=n_steps):
                for min_r in np.linspace(start=point_radii[0], stop=point_radii[1], num=n_steps):
                    if min_r < max_r:
                        point_annuli.append(self._get_annulus(point, max_r, min_r))

            annuli.append(point_annuli)
        return annuli

    def process_intrinsic_dimension_estimates(self):
        for query in self._queries:
            query.process_intrinsic_dimension_estimates()
