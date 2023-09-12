from data_processing.data_storage import *


def extract_query_and_data(word_collection, k):
    embeddings_path = word_collection.embeddings_path
    embeddings = load_bin(embeddings_path)

    query = np.array([word.embedding for word in word_collection.words.values()])

    keys = set()
    for q in query:
        most_similar = embeddings.similar_by_vector(vector=q, topn=(k + 1))
        keys.update([key for key, similarity in most_similar])

    data = np.array([embeddings[key] for key in keys])

    return query, data


def get_neighborhood(query, data, k):
    tree = KDTree(data)
    distances, indices = tree.query([query], k=(k + 1))
    indices = indices[0][1:] if distances[0][0] == 0 else indices[0][:-1]

    neighborhood = data[indices]
    return neighborhood
