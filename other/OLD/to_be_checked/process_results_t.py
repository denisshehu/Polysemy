from sample_generation import *
from results_processing.main_t import *

n = 10000
d_values = [2, 3]
r = 1
seed = 1

for d in d_values:
    input = sample_from_sphere(n=n, intrinsic_dimension=d, r=r, seed=seed)

    get_results(query=1000, input=input, max_dimension=d, seed=2)
