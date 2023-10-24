from utils.storage import *


def add_extra_dimensions(points, desired_dimension):
    if desired_dimension is not None:
        n, actual_dimension = points.shape
        extra_dimensions = np.zeros(shape=(n, (desired_dimension - actual_dimension)))
        points = np.hstack((points, extra_dimensions))

    return points


def translate(points, vector):
    return points - vector


def project_to_unit_circle(points, origin):
    points = translate(points, origin) if origin is not None else points
    for point in points:
        norm = np.linalg.norm(point)
        point *= 1 / norm
    return points


def scale(points, origin, scaler):
    points = translate(points, origin) if origin is not None else points
    points *= 1 / scaler
    return points


def filter_persistence_diagrams(persistence_diagrams, word=None):
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

    if word is not None:
        max_i = -1
        for i in range(len(filtered_persistence_diagrams)):
            if len(filtered_persistence_diagrams[i]) > 0:
                max_i = max(max_i, i)

        with open('C:\\Users\\its_d\\Desktop\\diagrams.txt', 'a') as file:
            file.write(f'{word}: {max_i} (euclidicity)\n')

    filtered_persistence_diagrams = [diagram for diagram in filtered_persistence_diagrams if len(diagram) > 0]
    return filtered_persistence_diagrams


def save_point_cloud(point_cloud, filename_prefix):
    if filename_prefix is not None:
        file_path = os.path.join(results_directory, f'{filename_prefix}_point_cloud.yaml')
        save_yaml(point_cloud, file_path)


def filter_embeddings(embeddings):
    filtered_keys = [key for key in embeddings.index_to_key if len(wordnet.synsets(key)) > 0 and not key.isdigit()]
    filtered_vectors = [embeddings[key] for key in filtered_keys]
    filtered_embeddings = KeyedVectors(vector_size=embeddings.vector_size)
    filtered_embeddings.add_vectors(filtered_keys, filtered_vectors)
    return filtered_embeddings
