from utils.imports import *


def add_extra_dimensions(points, spatial_dimension):
    if spatial_dimension is not None:
        n, intrinsic_dimension = points.shape
        extra_dimensions = np.zeros(shape=(n, (spatial_dimension - intrinsic_dimension)))
        points = np.hstack((points, extra_dimensions))

    return points


def sample_from_sphere(n, intrinsic_dimension, r, seed=None, spatial_dimension=None):
    np.random.seed(seed)

    points = np.random.normal(size=(n, intrinsic_dimension))
    for point in points:
        norm = np.linalg.norm(point)
        point *= r / norm

    points = add_extra_dimensions(points, spatial_dimension)
    return points


def sample_from_ball(n, intrinsic_dimension, r, seed=None, spatial_dimension=None):
    points = sample_from_sphere(n, (intrinsic_dimension + 2), r, seed)
    points = points[:, :-2]
    points = add_extra_dimensions(points, spatial_dimension)
    return points


def sample_from_singularity(n, intrinsic_dimension, r, angle_in_degrees, seed=None, spatial_dimension=None):
    axis = np.zeros(shape=intrinsic_dimension)
    axis[-1] = 1

    points = np.empty(shape=(0, intrinsic_dimension))
    threshold = math.cos(math.radians(angle_in_degrees))

    while points.shape[0] < n:
        points_ = sample_from_ball(n, intrinsic_dimension, r, seed)
        for point in points_:
            cosine_similarity = np.dot(point, axis) / np.linalg.norm(point)
            if abs(cosine_similarity) >= threshold:
                points = np.row_stack((points, point))

    points = points[:n, :]
    points = add_extra_dimensions(points, spatial_dimension)
    return points


def sample_from_annulus(n, intrinsic_dimension, max_r, min_r, seed=None, spatial_dimension=None):
    points = np.empty(shape=(0, intrinsic_dimension))

    while points.shape[0] < n:
        points_ = sample_from_ball(n, intrinsic_dimension, max_r, seed)
        for point in points_:
            norm = np.linalg.norm(point)
            if norm >= min_r:
                points = np.row_stack((points, point))

    points = points[:n, :]
    points = add_extra_dimensions(points, spatial_dimension)
    return points


def sample_from_intersecting_spheres(n1, intrinsic_dimension1, r1, n2, intrinsic_dimension2, r2, spatial_dimension=None,
                                     seed1=None, seed2=None):
    sphere1 = sample_from_sphere(n1, intrinsic_dimension1, r1, seed1, spatial_dimension)
    sphere2 = sample_from_sphere(n2, intrinsic_dimension2, r2, seed2, spatial_dimension)

    for point in sphere1:
        point[0] -= (r1 + r2)

    points = np.row_stack((sphere1, sphere2))
    return points

# def sample_from_pinched_torus(n, spacial_dimension, large_r, small_max_r, small_min_r, seed):
#     data = []
#
#     np.random.seed(seed)
#
#     pi = np.pi
#     omegas = np.random.uniform(low=0, high=(2 * pi), size=n)
#     thetas = np.random.uniform(low=0, high=(2 * pi), size=n)
#
#     for i in range(n):
#         u = omegas[i]
#         v = thetas[i]
#
#         if u <= pi:
#             r = small_max_r * (1 - u / pi) + small_min_r * u / pi
#         else:
#             r = small_min_r * (1 - (u - pi) / pi) + small_max_r * (u - pi) / pi
#
#         x = (large_r + r * np.cos(v)) * np.cos(u)
#         y = (large_r + r * np.cos(v)) * np.sin(u)
#         z = r * np.sin(v)
#
#         data.append(np.array([x, y, z]))
#
#     data = np.array(data)
#     data = np.hstack((data, np.zeros(shape=(data.shape[0], spacial_dimension - data.shape[1]))))
#     return data


# def sample_from_filled_cube(n, intrinsic_dimension, spatial_dimension, side_length, seed):
#     np.random.seed(seed)
#
#     half_length = side_length / 2
#     data = np.random.uniform(low=(-half_length), high=half_length, size=(n, intrinsic_dimension))
#
#     data = np.hstack((data, np.zeros(shape=(data.shape[0], spatial_dimension - intrinsic_dimension))))
#     return data
