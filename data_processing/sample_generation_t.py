from utils_t import *


def set_seed(seed):
    np.random.seed(seed)


def stack_dimensions(data, d_intrinsic, d_features):
    return np.hstack((data, np.zeros(shape=(data.shape[0], d_features - d_intrinsic))))


def sample_from_annulus(n, d_intrinsic, d_features, r_max, r_min, seed):
    data = []

    set_seed(seed)

    while len(data) < n:
        point = np.random.uniform(low=-r_max, high=r_max, size=d_intrinsic)
        norm = np.linalg.norm(point)
        if r_min <= norm <= r_max:
            data.append(point)

    data = np.array(data)
    data = stack_dimensions(data, d_intrinsic, d_features)
    return data


def sample_from_ball(n, d_intrinsic, d_features, r, seed):
    return sample_from_annulus(n=n, d_intrinsic=d_intrinsic, d_features=d_features, r_max=r, r_min=0, seed=seed)


def sample_from_sphere(n, d_intrinsic, d_features, r, seed):
    set_seed(seed)

    data = np.random.randn(n, d_intrinsic)
    data = r * data / np.sqrt(np.sum(data ** 2, 1)[:, None])
    data = stack_dimensions(data, d_intrinsic, d_features)
    return data


def sample_from_intersecting_spheres(n1, d_intrinsic1, r1, seed1, n2, d_intrinsic2, r2, seed2, d_features):
    sphere1 = sample_from_sphere(n=n1, d_intrinsic=d_intrinsic1, d_features=d_features, r=r1, seed=seed1)
    sphere2 = sample_from_sphere(n=n2, d_intrinsic=d_intrinsic2, d_features=d_features, r=r2, seed=seed2)

    for i in range(len(sphere1)):
        sphere1[i][0] -= r1 + r2

    data = np.vstack((sphere1, sphere2))
    return data


def sample_from_pinched_torus(n, d_features, r_max, r_min_max, r_min_min, seed):
    data = []

    set_seed(seed)

    pi = np.pi
    omegas = np.random.uniform(low=0, high=(2 * pi), size=n)
    thetas = np.random.uniform(low=0, high=(2 * pi), size=n)

    for i in range(n):
        u = omegas[i]
        v = thetas[i]

        if u <= pi:
            r = r_min_max * (1 - u / pi) + r_min_min * u / pi
        else:
            r = r_min_min * (1 - (u - pi) / pi) + r_min_max * (u - pi) / pi

        x = (r_max + r * np.cos(v)) * np.cos(u)
        y = (r_max + r * np.cos(v)) * np.sin(u)
        z = r * np.sin(v)

        data.append(np.array([x, y, z]))

    data = np.array(data)
    data = stack_dimensions(data, data.shape[1], d_features)
    return data


def sample_from_pinched_surface(n, d_intrinsic, d_features, r, pinch_h, pinch_r, seed):
    data = []

    set_seed(seed)

    while len(data) < n:
        point = np.random.uniform(low=-r, high=r, size=(d_intrinsic - 1))
        norm = np.linalg.norm(point)
        if norm <= r:
            if norm <= pinch_r:
                height = (1 - norm / pinch_r) * pinch_h
                point = np.append(point, height)
            else:
                point = np.append(point, 0)
            data.append(point)

    data = np.array(data)
    data = stack_dimensions(data, d_intrinsic, d_features)
    return data


def sample_from_cube(n, d_intrinsic, d_features, side_length, seed):
    set_seed(seed)

    half_length = side_length / 2
    data = np.random.uniform(low=-half_length, high=half_length, size=(n, d_intrinsic))
    data = stack_dimensions(data, d_intrinsic, d_features)
    return data


def sample_from_pyramid(n, d_intrinsic, d_features, base_length, height, seed, is_upside_down):
    data = []

    set_seed(seed)

    heights = np.random.uniform(low=0, high=height, size=n)

    for height_ in heights:
        side_length = height_ * base_length if is_upside_down else (height - height_) * base_length
        half_length = side_length / 2
        point = np.random.uniform(low=-half_length, high=half_length, size=(d_intrinsic - 1))
        point = np.append(point, height_)
        data.append(point)

    data = np.array(data)
    data = stack_dimensions(data, d_intrinsic, d_features)
    return data


# TODO: does not work for pyramids of different dimensions
def sample_from_singularity(n1, d_intrinsic1, base_length1, height1, seed1,
                            n2, d_intrinsic2, base_length2, height2, seed2, d_features):
    pyramid1 = sample_from_pyramid(n=n1, d_intrinsic=d_intrinsic1, d_features=d_features, base_length=base_length1,
                                   height=height1, seed=seed1, is_upside_down=False)
    pyramid2 = sample_from_pyramid(n=n2, d_intrinsic=d_intrinsic2, d_features=d_features, base_length=base_length2,
                                   height=height2, seed=seed2, is_upside_down=True)

    for i in range(len(pyramid2)):
        pyramid2[i][d_intrinsic2 - 1] += height1

    data = np.vstack((pyramid1, pyramid2))
    return data
