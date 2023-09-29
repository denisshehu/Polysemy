from utils.imports import *


def translate(points, vector):
    return points - vector


def project_to_unit_circle(points, origin):
    points = translate(points, origin) if origin is not None else points
    for point in points:
        norm = np.linalg.norm(point)
        point *= 1 / norm
    return points
