import os

import numpy as np

from utils.storage import save_yaml
from utils.utils import results_directory


# def compute_persistence_diagrams(data, maximum_dimension):
#     return ripser_parallel(X=data, maxdim=maximum_dimension, collapse_edges=True)['dgms']


def scale_annulus(annulus, scaler, point=None):
    translated_annulus = (annulus - point) if point is not None else annulus
    scaled_annulus = translated_annulus / scaler
    return scaled_annulus


def filter_persistence_diagrams(persistence_diagrams, remove_empty_diagrams=True):
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

    if remove_empty_diagrams:
        return [diagram for diagram in filtered_persistence_diagrams if len(diagram) > 0]
    else:
        return filtered_persistence_diagrams
