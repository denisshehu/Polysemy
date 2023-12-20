from utils.sample_generation import *
from utils.visualization_generation import *

n = 300
intrinsic_dimensions = [(i + 1) for i in range(20)]
r = 1
angle_in_degrees = 30
seed = 1
ambient_dimension = 300

for intrinsic_dimension in intrinsic_dimensions:
    sample = sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed, ambient_dimension)
    save_ndarray(sample, os.path.join(samples_directory, f'cones_n{n}_d{intrinsic_dimension}.csv'))
