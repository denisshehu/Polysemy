from utils.variables import *


def load_xml(file_path):
    element_tree = ElementTree.parse(file_path)
    return element_tree


# def save_bin(data, file_path):
#     data.save_word2vec_format(file_path, binary=True)


def load_embeddings(file_path):
    if file_path == fasttext_embeddings_path:
        embeddings = FastText.load_fasttext_format(file_path).wv
    elif file_path == glove_embeddings_path:
        embeddings = KeyedVectors.load_word2vec_format(file_path, no_header=True)
    elif file_path == word2vec_embeddings_path:
        embeddings = KeyedVectors.load_word2vec_format(file_path, binary=True)
    else:
        embeddings = None

    return embeddings


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


def save_csv(data, file_path):
    data.to_csv(file_path, index=False)


def load_csv(file_path):
    data = pd.read_csv(file_path)
    return data


def save_point_cloud(point_cloud, filename_prefix):
    filename_prefix = f'{filename_prefix}_' if filename_prefix is not None else ''
    point_cloud_path = os.path.join(results_directory, f'{filename_prefix}point_cloud.yaml')
    save_yaml(point_cloud, point_cloud_path)

# def load_words():
#     return np.loadtxt(os.path.join(project_directory, 'words.txt'), dtype=str).tolist()
