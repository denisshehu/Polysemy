from utils.main import *


def extract_evaluation_set(evaluation_set_path):
    evaluation_set = load_txt(evaluation_set_path)
    evaluation_set = [line.replace('\n', '').split('\t') for line in evaluation_set if '#' not in line[0]]

    for line in evaluation_set:
        line[-1] = float(line[-1])

    if 'ws.txt' in evaluation_set_path:
        evaluation_set = [line[1:] for line in evaluation_set]

    return evaluation_set


def evaluate():
    pearson, spearman = list(), list()

    for embeddings_name, embeddings_path in [('Word2vec', word2vec_embeddings_path),
                                             ('fastText', fasttext_embeddings_path),
                                             ('GloVe', glove_embeddings_path)]:
        embeddings = load_embeddings(embeddings_path)
        embeddings_pearson, embeddings_spearman = [embeddings_name], [embeddings_name]

        for evaluation_set_name, evaluation_set_path in [('ws', ws_path), ('similarity', ws_similarity_path),
                                                         ('relatedness', ws_relatedness_path)]:
            true, pred = list(), list()

            evaluation_set = extract_evaluation_set(evaluation_set_path)
            for instance in evaluation_set:
                try:
                    word1, word2, value = instance
                    cosine_similarity = compute_cosine_similarity(embeddings[word1], embeddings[word2])
                    true.append(value)
                    pred.append(cosine_similarity)
                except:
                    pass

            true, pred = np.array(true), np.array(pred)
            pearson_correlation_coefficient, p_value = pearsonr(true, pred)
            spearman_correlation_coefficient, p_value = spearmanr(true, pred)
            embeddings_pearson.append(pearson_correlation_coefficient)
            embeddings_spearman.append(spearman_correlation_coefficient)

            point_sizes = len(true) * [5]
            plot_scatterplot(true, pred, 'Ground truth', 'Cosine similarity',
                             -0.5, 10.5, -0.05, 1.05, point_sizes,
                             figure_name=f'{embeddings_name.lower()}-{evaluation_set_name.lower()}')

        pearson.append(embeddings_pearson)
        spearman.append(embeddings_spearman)

    column_names = ['Model', 'WordSim353', 'WordSim353 (Similarity)', 'WordSim353 (Relatedness)']
    save_csv(pd.DataFrame(pearson, columns=column_names), os.path.join(results_directory, 'pearson.csv'))
    save_csv(pd.DataFrame(spearman, columns=column_names), os.path.join(results_directory, 'spearman.csv'))
