from data_processing.data_storage import *


def generate_output(query, input, n_neighbors, max_dimension, n_steps, batch_size, seed, filename_prefix,
                    keep_terminal_open):
    n = batch_size if batch_size is not None else len(input)
    n_query_points = query if isinstance(query, int) else None
    filename = construct_filename(filename_prefix=filename_prefix, n=n, q=n_query_points, k=n_neighbors, d=max_dimension,
                                  s=n_steps, seed=seed)

    input_path = os.path.join(inputs_directory, f'{filename}input.txt')
    save_ndarray(input, input_path)

    if n_query_points is None:
        query_path = os.path.join(queries_directory, f'{filename}query.txt')
        save_ndarray(query, query_path)
        p = f'-p \"{query_path}\"'
    else:
        p = ''

    output_path = os.path.join(outputs_directory, f'{filename}output.csv')

    keep = 'k' if keep_terminal_open else 'c'
    q = f'-q {n_query_points}' if n_query_points is not None else ''
    seed_ = f'--seed {seed}' if seed is not None else ''

    command = f'start cmd /{keep} \"cd \"{tardis_directory}\" & \"{activate_path}\" & ' \
              f'python cli.py \"{input_path}\" {p} -k {n_neighbors} -d {max_dimension} --num-steps {n_steps} -b {n} ' \
              f'{q} {seed_} > \"{output_path}\"\"'

    os.system(command)

    wait_until_completion(output_path)
    return filename


def construct_filename(**kwargs):
    filename = ''

    for key, value in kwargs.items():
        if value is not None:
            if key == 'filename_prefix':
                filename += f'{value}_'
            elif isinstance(value, float):
                filename += f'{key}{value:.1f}_'
            else:
                filename += f'{key}{value}_'

    return filename


def wait_until_completion(output_path):
    while not os.path.exists(output_path):
        continue

    completed = False
    while not completed:
        time.sleep(1)
        completed = os.path.getsize(output_path) != 0
