from data_processing.sample_generation_t import *
from results_processing.main_t import *

n = 10000
d_values = [2, 3]
r = 1
seed = 1

for d in d_values:
    input = sample_from_sphere(n=n, d=d, r=r, seed=seed)

    get_results(query=1000, input=input, max_dimension=d, seed=2)
