from utils.imports import *


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


def filter_persistence_diagrams(persistence_diagrams):
    filtered_persistence_diagrams = []

    threshold = 0.0
    for persistence_diagram in persistence_diagrams:
        filtered_persistence_diagram = []

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
