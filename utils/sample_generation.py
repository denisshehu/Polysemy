from utils.functions import *


def sample_from_sphere(n, intrinsic_dimension, r, seed=None, ambient_dimension=None):
    np.random.seed(seed)

    points = np.random.normal(size=(n, (intrinsic_dimension + 1)))
    for point in points:
        norm = np.linalg.norm(point)
        point *= r / norm

    points = add_extra_dimensions(points, ambient_dimension)
    return points


def sample_from_ball(n, intrinsic_dimension, r, seed=None, ambient_dimension=None):
    points = sample_from_sphere(n, ((intrinsic_dimension - 1) + 2), r, seed)
    points = points[:, :-2]
    points = add_extra_dimensions(points, ambient_dimension)
    return points


def sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed=None, ambient_dimension=None):
    np.random.seed(seed)

    axis = np.zeros(shape=intrinsic_dimension)
    axis[-1] = 1

    points = np.empty(shape=(0, intrinsic_dimension))
    threshold = math.cos(math.radians(angle_in_degrees))

    while points.shape[0] < n:
        seed_ = np.random.randint(np.iinfo(np.int32).max)
        points_ = sample_from_ball(n, intrinsic_dimension, r, seed_)

        for point in points_:
            cosine_similarity = np.dot(point, axis) / np.linalg.norm(point)
            if abs(cosine_similarity) >= threshold:
                points = np.row_stack((points, point))

    points = points[:n, :]
    points = add_extra_dimensions(points, ambient_dimension)
    return points


def sample_from_intersecting_planes(n1, r1, n2, r2, intrinsic_dimension, seed1=None, seed2=None,
                                    ambient_dimension=None):
    plane1 = sample_from_ball(n1, intrinsic_dimension, r1, seed1, ambient_dimension)
    plane2 = sample_from_ball(n2, intrinsic_dimension, r2, seed2, (ambient_dimension - 1))
    plane2 = np.hstack((np.zeros(shape=(plane2.shape[0], 1)), plane2))

    points = np.row_stack((plane1, plane2))
    return points


def sample_from_annulus(n, intrinsic_dimension, max_r, min_r, seed=None, ambient_dimension=None):
    np.random.seed(seed)

    points = np.empty(shape=(0, intrinsic_dimension))

    while points.shape[0] < n:
        seed_ = np.random.randint(np.iinfo(np.int32).max)
        points_ = sample_from_ball(n, intrinsic_dimension, max_r, seed_)

        for point in points_:
            norm = np.linalg.norm(point)
            if norm >= min_r:
                points = np.row_stack((points, point))

    points = points[:n, :]
    points = add_extra_dimensions(points, ambient_dimension)
    return points


def sample_from_intersecting_spheres(n1, intrinsic_dimension1, r1, n2, intrinsic_dimension2, r2, ambient_dimension,
                                     proportion=1, seed1=None, seed2=None):
    sphere1 = sample_from_sphere(n1, intrinsic_dimension1, r1, seed1, ambient_dimension)
    sphere2 = sample_from_sphere(n2, intrinsic_dimension2, r2, seed2, ambient_dimension)

    for point in sphere1:
        point[0] -= proportion * r1
    for point in sphere2:
        point[0] += proportion * r2

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
