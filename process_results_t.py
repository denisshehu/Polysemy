from data_processing.sample_generation import *
from results_processing.output_generation import *
from results_processing.a import *

n_values = [10 ** (i + 1) for i in range(3)]
d = 2
r = 1
seed = 1

for n in n_values:
    input = sample_from_sphere(n=n, d=d, r=r, seed=seed)

    output_path = generate_output(input, n_query_points=1, seed=2)
    try:
        visualize_output(output_path)
    except:
        pass