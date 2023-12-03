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
    summary = list()

    for embeddings_name, embeddings_path in [('Word2vec', word2vec_embeddings_path),
                                             ('fastText', fasttext_embeddings_path),
                                             ('GloVe', glove_embeddings_path)]:
        embeddings = load_embeddings(embeddings_path)
        embeddings_summary = [embeddings_name]

        for evaluation_set_name, evaluation_set_path in [('ws', ws_path), ('ws_similarity', ws_similarity_path),
                                                         ('ws_relatedness', ws_relatedness_path)]:
            true = list()
            pred = list()

            evaluation_set = extract_evaluation_set(evaluation_set_path)
            for instance in evaluation_set:
                try:
                    word1, word2, value = instance
                    cosine_similarity = compute_cosine_similarity(embeddings[word1], embeddings[word2])
                    true.append(value)
                    pred.append(cosine_similarity)
                except:
                    pass

            correlation_coefficient, p_value = pearsonr(true, pred)
            embeddings_summary.append(correlation_coefficient)

            point_sizes = len(true) * [5]
            plot_scatterplot(true, pred, 'Ground truth', 'Cosine similarity',
                             -0.5, 10.5, -0.05, 1.05, point_sizes, figure_context='science',
                             figure_name=f'{embeddings_name.lower()}_{evaluation_set_name.lower()}')

        summary.append(embeddings_summary)

    column_names = ['Model', 'WordSim353', 'WordSim353 (Similarity)', 'WordSim353 (Relatedness)']
    save_csv(pd.DataFrame(summary, columns=column_names), os.path.join(results_directory, 'summary.csv'))
