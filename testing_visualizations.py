import winsound

from models.point_cloud import *
from methods import topological_polysemy, gad, euclidicity
from methods.intrinsic_dimension_estimators import danco

n = 10000
intrinsic_dimension = 2
r = 1
seed = 1
points = sample_from_sphere(n, intrinsic_dimension, r, seed)
filename_prefix = 'visualization_testing'

point_cloud = PointCloud()
point_cloud.random_constructor(points, 100, seed=1)

topological_polysemy.calculate(point_cloud, 100, filename_prefix=filename_prefix)
visualize_topological_polysemy(point_cloud, filename_prefix)

danco.estimate(point_cloud, 10, 20, filename_prefix)
visualize_dimension(point_cloud, filename_prefix)

# gad.detect(point_cloud, 100, filename_prefix=filename_prefix)
# visualize_classification(point_cloud, filename_prefix)

euclidicity.calculate(point_cloud, 100, filename_prefix=filename_prefix)
visualize_euclidicity(point_cloud, filename_prefix)

winsound.Beep(500, 3000)
