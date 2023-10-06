from utils.main import *


class Query:

    def __init__(self, identifier, point, word=None):
        self._identifier = identifier
        self._point = point

        self._initial_intrinsic_dimension_estimates = dict()
        self._filtered_intrinsic_dimension_estimates = None
        self._intrinsic_dimension = None

        self._initial_classifications = None
        self._classification = None

        self._euclidicity_estimates = None
        self._euclidicity = None

        self._topological_polysemy = None

        self._word = word
        self._n_senses = len(wn.synsets(word)) if word is not None else None

    @property
    def identifier(self):
        return self._identifier

    @property
    def point(self):
        return self._point

    # @property
    # def initial_intrinsic_dimension_estimates(self):
    #     return self._initial_intrinsic_dimension_estimates

    # @property
    # def filtered_intrinsic_dimension_estimates(self):
    #     return self._filtered_intrinsic_dimension_estimates

    @property
    def intrinsic_dimension(self):
        return self._intrinsic_dimension

    @intrinsic_dimension.setter
    def intrinsic_dimension(self, intrinsic_dimension):
        self._intrinsic_dimension = intrinsic_dimension

    # @property
    # def initial_classifications(self):
    #     return self._initial_classifications

    @property
    def classification(self):
        return self._classification

    @classification.setter
    def classification(self, classification):
        self._classification = classification

    # @property
    # def euclidicity_estimates(self):
    #     return self._euclidicity_estimates

    # @euclidicity_estimates.setter
    # def euclidicity_estimates(self, euclidicity_estimates):
    #     self._euclidicity_estimates = euclidicity_estimates

    @property
    def euclidicity(self):
        return self._euclidicity

    @euclidicity.setter
    def euclidicity(self, euclidicity):
        self._euclidicity = euclidicity

    @property
    def topological_polysemy(self):
        return self._topological_polysemy

    @topological_polysemy.setter
    def topological_polysemy(self, topological_polysemy):
        self._topological_polysemy = topological_polysemy

    @property
    def word(self):
        return self._word

    @property
    def n_senses(self):
        return self._n_senses

    def add_intrinsic_dimension_estimate(self, key, estimate):
        self._initial_intrinsic_dimension_estimates[key] = estimate

    def process_intrinsic_dimension_estimates(self):
        self._filter_intrinsic_dimension_estimates()
        self._calculate_intrinsic_dimension()

    def _filter_intrinsic_dimension_estimates(self):
        sorted_estimates = sorted(self._initial_intrinsic_dimension_estimates.items(), key=lambda item: item[1])
        n_estimates = len(sorted_estimates)
        quartile_index = n_estimates // 4

        if quartile_index == 0:
            self._filtered_intrinsic_dimension_estimates = self._initial_intrinsic_dimension_estimates
        else:
            filtered_estimates = dict(sorted_estimates[quartile_index:(-quartile_index)])
            self._filtered_intrinsic_dimension_estimates = filtered_estimates

    def _calculate_intrinsic_dimension(self):
        estimates = self._filtered_intrinsic_dimension_estimates.values()
        intrinsic_dimension = round(sum(estimates) / len(estimates))

        self._intrinsic_dimension = intrinsic_dimension

    def process_initial_classifications(self, initial_classifications):
        self._initial_classifications = initial_classifications

        unique_values, counts = np.unique(list(initial_classifications.values()), return_counts=True)
        index_most_common_value = np.argmax(counts)
        self._classification = unique_values[index_most_common_value]
        print(unique_values, counts)
        print(index_most_common_value)
        print(self._classification)
        print

    def process_euclidicity_estimates(self, euclidicity_estimates):
        self._euclidicity_estimates = euclidicity_estimates
        self._euclidicity = sum(euclidicity_estimates.values()) / len(euclidicity_estimates)
