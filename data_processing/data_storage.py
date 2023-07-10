from utils import *


def load_xml(file_path):
    element_tree = ElementTree.parse(file_path)
    return element_tree


def load_bin(file_path):
    keyed_vectors = KeyedVectors.load_word2vec_format(file_path, binary=True)
    return keyed_vectors


def save_txt(data, file_path):
    with open(file_path, 'w') as file:
        file.writelines(data)


def load_txt(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return data


def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)


def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.Loader)
    return data


def construct_filename(**kwargs):
    filename = ''
    for key, value in kwargs.items():
        if value is not None:
            if isinstance(value, float):
                filename += f'{key}{value:.1f}_'
            else:
                filename += f'{key}{value}_'
    filename = filename[:-1] + '.txt'
    return filename


def save_ndarray(ndarray, directory, **kwargs):
    filename = construct_filename(**kwargs)
    file_path = os.path.join(directory, filename)
    np.savetxt(file_path, ndarray)


def load_ndarray(directory, **kwargs):
    filename = construct_filename(**kwargs)
    file_path = os.path.join(directory, filename)
    ndarray = np.loadtxt(file_path)
    return ndarray
