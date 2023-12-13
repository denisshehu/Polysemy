from utils.main import *


def calculate(point_cloud, neighborhood_size, min_to_max_s_ratio=1, r_to_s_ratio=0, n_steps=1, filename_prefix=None):
    calculate_in_parallel(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)
    save_point_cloud(point_cloud, filename_prefix)


def calculate_in_parallel(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps):
    annuli = point_cloud.get_annuli(neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)

    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(_calculate)(query, query_annuli)
        for query, query_annuli in zip(point_cloud.queries, annuli)
    )
    results = {key: value for key, value in results}

    for query in point_cloud.queries:
        query.process_topological_polysemy_estimates(results[query.identifier])


def _calculate(query, query_annuli):
    estimates = dict()
    for annulus, s, r in query_annuli:
        if len(annulus) != 0:
            projected_annulus = project_to_unit_sphere(annulus, query.point)
            zeroth_persistence_diagram = ripser.ripser(projected_annulus, maxdim=0)['dgms'][0]
            estimate = wasserstein_distance(X=zeroth_persistence_diagram, Y=np.array([[0, np.inf]]))
            estimates[(s, r)] = estimate

    return query.identifier, estimates
