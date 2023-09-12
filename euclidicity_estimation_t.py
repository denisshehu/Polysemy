import winsound
from data_processing.sample_generation_t import *
from results_processing.main_t import *
from results_processing.extra_t import *

n = 1000
k = 50
d_values = [20]
D = 300
side_length = 1
base_length = 0.2
height = 1
seed = 1

for d in d_values:
    query_regular = np.zeros((1, D))
    input_regular = sample_from_cube(n=n, d_intrinsic=d, d_features=D, side_length=side_length, seed=seed)
    input_regular = np.concatenate((input_regular, query_regular))

    for max_d in range(d - 10, d + 11):
        max_d = max(max_d, 0)
        if max_d == 11:
            get_results(query_regular, input_regular, n_neighbors_euclidicity=k, max_dimension=max_d, seed=seed,
                        filename_prefix=f'regular_trued{d}', keep_terminal_open=False)

    query_singularity = np.zeros((1, D))
    query_singularity[0][d - 1] = height
    input_singularity = sample_from_singularity(n=round(n / 2), d=d, D=D, base_length=base_length,
                                                height=height, seed=seed)
    input_singularity = np.concatenate((input_singularity, query_singularity))

    # for max_d in range(d - 10, d + 11):
    #     max_d = max(max_d, 0)
    #     get_results(query_singularity, input_singularity, n_neighbors=k, max_dimension=max_d, seed=seed,
    #                 filename_prefix=f'singularity_trued{d}', keep_terminal_open=False)

winsound.Beep(500, 3000)
