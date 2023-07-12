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


def save_ndarray(data, file_path):
    np.savetxt(file_path, data)


def load_ndarray(file_path):
    data = np.loadtxt(file_path)
    return data


def load_csv(file_path):
    data = pd.read_csv(file_path)
    return data
