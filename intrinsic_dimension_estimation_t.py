import winsound
from data_processing.sample_generation_t import *
from results_processing.main_t import *
from results_processing.extra_t import *

estimator = 'danco'
actual_dimension = 300
n = 1000
k_values = [(i + 1) for i in range(90)]
d_values = [5 * (i + 1) for i in range(4, 20)]
side_length = 1
seed = 1

for k in k_values:
    for d in d_values:
        max_dimension = d
        filename_prefix = f'{estimator}_{d}'

        query = np.zeros((1, actual_dimension))
        input = sample_from_cube(n=n, d_intrinsic=d, side_length=side_length, seed=seed)
        input = np.hstack((input, np.zeros(shape=(input.shape[0], actual_dimension - d))))
        input = np.concatenate((input, query))

        get_results(query, input, n_neighbors_euclidicity=k, max_dimension=max_dimension, seed=seed,
                    filename_prefix=filename_prefix, keep_terminal_open=False)

winsound.Beep(500, 3000)
