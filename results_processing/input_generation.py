from utils import *


def generate_test_data(n, dimension, radius, pinch_height, pinch_radius, seed):
    data = []

    point = np.zeros(shape=(dimension - 1))
    point = np.append(point, pinch_height)
    data.append(point)

    if seed is not None:
        np.random.seed(seed)

    while len(data) < n + 1:
        point = np.random.uniform(low=-radius, high=radius, size=(dimension - 1))
        norm = np.linalg.norm(point)
        if norm <= 1.0:
            if norm <= pinch_radius:
                height = (1 - norm / pinch_radius) * pinch_height
                point = np.append(point, height)
            else:
                point = np.append(point, 0.0)
            data.append(point)

    data = np.array(data)
    return data
