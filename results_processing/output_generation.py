from data_processing.data_storage import *


def construct_filename(**kwargs):
    filename = ''

    for key, value in kwargs.items():
        if value is not None:
            if key == 'function':
                filename += f'{value}_'
            elif isinstance(value, float):
                filename += f'{key}{value:.1f}_'
            else:
                filename += f'{key}{value}_'

    return filename


def generate_output(input, n_neighbors=50, max_dimension=2, n_steps=10, batch_size=None,
                    n_query_points=None, query_points=None, seed=None, function=None, keep=True):
    n = batch_size if batch_size is not None else len(input)
    keep_ = 'k' if keep else 'c'
    q_ = f'-q {n_query_points}' if n_query_points is not None else ''
    seed_ = f'--seed {seed}' if seed is not None else ''
    filename = construct_filename(function=function, n=n, q=n_query_points,
                                  k=n_neighbors, d=max_dimension, s=n_steps, seed=seed)

    input_path = os.path.join(results_directory, f'{filename}input.txt')
    save_ndarray(input, input_path)

    if query_points is not None:
        query_points_path = os.path.join(results_directory, f'{filename}query_points.txt')
        save_ndarray(query_points, query_points_path)
        p_ = f'-p \"{query_points_path}\"'
    else:
        p_ = ''

    output_path = os.path.join(results_directory, f'{filename}output.csv')

    command = f'start cmd /{keep_} \"cd \"{tardis_directory}\" & \"{activate_path}\" & ' \
              f'python cli.py \"{input_path}\" {p_} -k {n_neighbors} -d {max_dimension} --num-steps {n_steps} -b {n} ' \
              f'{q_} {seed_} > \"{output_path}\"\"'
    os.system(command)

    return output_path
