from utils.storage import *


def add_extra_dimensions(points, desired_dimension):
    if desired_dimension is not None:
        n, actual_dimension = points.shape
        extra_dimensions = np.zeros(shape=(n, (desired_dimension - actual_dimension)))
        points = np.hstack((points, extra_dimensions))

    return points


def translate(points, vector):
    return points - vector


def project_to_unit_sphere(points, origin):
    points = translate(points, origin) if origin is not None else points
    for point in points:
        norm = np.linalg.norm(point)
        point *= 1 / norm
    return points


def scale(points, origin, scaler):
    points = translate(points, origin) if origin is not None else points
    points *= 1 / scaler
    return points


def filter_persistence_diagrams_dynamic(persistence_diagrams):
    filtered_persistence_diagrams = list()

    threshold = 0.0
    for persistence_diagram in persistence_diagrams:
        filtered_persistence_diagram = list()

        diagram_highest_persistence = 0.0
        for feature in persistence_diagram:
            birth = feature[0]
            death = feature[1]
            if death != np.inf:
                persistence = death - birth
                if persistence >= threshold:
                    filtered_persistence_diagram.append(feature)
                    diagram_highest_persistence = max(diagram_highest_persistence, persistence)
            else:
                filtered_persistence_diagram.append(feature)

        filtered_persistence_diagrams.append(np.array(filtered_persistence_diagram))
        threshold = max(threshold, diagram_highest_persistence)

    filtered_persistence_diagrams = [diagram for diagram in filtered_persistence_diagrams if len(diagram) > 0]
    return filtered_persistence_diagrams


def filter_persistence_diagrams_constant(persistence_diagrams, threshold):
    filtered_persistence_diagrams = list()

    for persistence_diagram in persistence_diagrams:
        filtered_persistence_diagram = list()

        for feature in persistence_diagram:
            birth = feature[0]
            death = feature[1]
            if death != np.inf:
                persistence = death - birth
                if persistence >= threshold:
                    filtered_persistence_diagram.append(feature)
            else:
                filtered_persistence_diagram.append(feature)

        filtered_persistence_diagrams.append(np.array(filtered_persistence_diagram))

    filtered_persistence_diagrams = [diagram for diagram in filtered_persistence_diagrams if len(diagram) > 0]
    return filtered_persistence_diagrams


def save_point_cloud(point_cloud, filename_prefix):
    if filename_prefix is not None:
        file_path = os.path.join(results_directory, f'{filename_prefix}_point_cloud.yaml')
        save_yaml(point_cloud, file_path)


def filter_embeddings(embeddings):
    filtered_embeddings = dict()
    for key in embeddings.index_to_key:
        if len(wordnet.synsets(key)) > 0 and not key.isdigit():
            lowercase_key = key.lower()
            if lowercase_key not in filtered_embeddings.keys():
                filtered_embeddings[lowercase_key] = embeddings[key]

    keyed_vectors = KeyedVectors(vector_size=embeddings.vector_size)
    keyed_vectors.add_vectors(list(filtered_embeddings.keys()), list(filtered_embeddings.values()))
    return keyed_vectors


def compute_cosine_similarity(vector1, vector2):
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
