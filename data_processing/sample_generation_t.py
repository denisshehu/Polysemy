from utils_t import *


def set_seed(seed):
    np.random.seed(seed)


def sample_from_annulus(n, d, R, r, seed):
    data = []

    set_seed(seed)

    while len(data) < n:
        point = np.random.uniform(low=-R, high=R, size=d)
        norm = np.linalg.norm(point)
        if r <= norm <= R:
            data.append(point)

    data = np.array(data)
    return data


def sample_from_ball(n, d, r, seed):
    return sample_from_annulus(n=n, d=d, R=r, r=0.0, seed=seed)


def sample_from_cube(n, d, D, side_length, seed):
    set_seed(seed)

    half_length = side_length / 2
    data = np.random.uniform(low=-half_length, high=half_length, size=(n, d))
    data = np.hstack((data, np.zeros(shape=(len(data), D - d))))
    return data


def sample_from_sphere(n, d, r, seed):
    set_seed(seed)

    data = np.random.randn(n, d)
    data = r * data / np.sqrt(np.sum(data ** 2, 1)[:, None])
    return data


def sample_from_intersecting_spheres(n1, d1, r1, seed1, n2, d2, r2, seed2):
    sphere1 = sample_from_sphere(n=n1, d=d1, r=r1, seed=seed1)
    sphere2 = sample_from_sphere(n=n2, d=d2, r=r2, seed=seed2)

    if d1 > d2:
        zeros = np.zeros(shape=(sphere2.shape[0], d1 - d2))
        sphere2 = np.hstack((sphere2, zeros))
    elif d1 < d2:
        zeros = np.zeros(shape=(sphere1.shape[0], d2 - d1))
        sphere1 = np.hstack((sphere1, zeros))

    for i in range(len(sphere1)):
        sphere1[i][0] -= r1 + r2

    data = np.vstack((sphere1, sphere2))
    return data


def sample_from_pinched_torus(n, R, r_max, r_min, seed):
    data = []

    set_seed(seed)

    pi = np.pi
    omegas = np.random.uniform(low=0, high=(2 * pi), size=n)
    thetas = np.random.uniform(low=0, high=(2 * pi), size=n)

    for i in range(n):
        u = omegas[i]
        v = thetas[i]

        if u <= pi:
            r = r_max * (1 - u / pi) + r_min * u / pi
        else:
            r = r_min * (1 - (u - pi) / pi) + r_max * (u - pi) / pi

        x = (R + r * np.cos(v)) * np.cos(u)
        y = (R + r * np.cos(v)) * np.sin(u)
        z = r * np.sin(v)

        data.append(np.array([x, y, z]))

    data = np.array(data)
    return data


def sample_from_pinched_surface(n, d, r, pinch_h, pinch_r, seed):
    data = []

    set_seed(seed)

    while len(data) < n:
        point = np.random.uniform(low=-r, high=r, size=d)
        norm = np.linalg.norm(point)
        if norm <= r:
            if norm <= pinch_r:
                height = (1 - norm / pinch_r) * pinch_h
                point = np.append(point, height)
            else:
                point = np.append(point, 0.0)
            data.append(point)

    data = np.array(data)
    return data


def sample_from_singularity(n, d, D, base_length, height, seed):
    data = []

    set_seed(seed)

    heights = np.random.uniform(low=0.0, high=height, size=n)

    for h in heights:
        side_length = (1 - h) * base_length
        half_length = side_length / 2
        point = np.random.uniform(low=-half_length, high=half_length, size=(d - 1))
        point = np.append(point, h)
        data.append(point)

    heights = np.random.uniform(low=0.0, high=height, size=n)

    for h in heights:
        side_length = h * base_length
        half_length = side_length / 2
        point = np.random.uniform(low=-half_length, high=half_length, size=(d - 1))
        point = np.append(point, height + h)
        data.append(point)

    data = np.hstack((data, np.zeros(shape=(len(data), D - d))))

    data = np.array(data)
    return data
