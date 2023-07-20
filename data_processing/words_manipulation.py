from utils import *


def filter_by_membership(words, attribute, values_list, negate=False):
    data = dict()

    for word in words.values():
        value = getattr(word, attribute)
        if values_list == [None]:
            if (not negate and value is None) or (negate and value is not None):
                data[word.value] = word
        else:
            if (not negate and value in values_list) or (negate and value not in values_list):
                data[word.value] = word

    return data


def filter_by_range(words, attribute, min_value=None, max_value=None):
    data = dict()

    for word in words.values():
        value = getattr(word, attribute)

        if None not in (min_value, max_value):
            if min_value <= value <= max_value:
                data[word.value] = word
        elif min_value is not None:
            if value >= min_value:
                data[word.value] = word
        elif max_value is not None:
            if value <= max_value:
                data[word.value] = word

    return data


def get_words_with_embedding(words):
    words_with_embedding = filter_by_membership(words, 'embedding', [None], True)
    return words_with_embedding


def normalize(embedding):
    norm = np.linalg.norm(embedding)
    normalized_embedding = embedding / norm
    return normalized_embedding


def get_embeddings(words):
    if isinstance(words, dict):
        words_with_embedding = get_words_with_embedding(words)
        embeddings = np.array([normalize(word.embedding) for word in words_with_embedding.values()])
    else:
        embeddings = np.array([normalize(word.embedding) for word in words])
    return embeddings


def get_monosemes(words):
    words_with_embedding = get_words_with_embedding(words)
    monosemes = filter_by_range(words_with_embedding, 'n_senses', max_value=1)
    monosemes = sorted(monosemes.values(), key=lambda word: word.count, reverse=True)
    return monosemes
