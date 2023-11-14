def fix_sco_corpus():
    data = load_txt(sco_corpus_path)
    data.insert(1, '<root>\n')
    data.append('</root>\n')
    save_txt(data, fixed_sco_corpus_path)


def normalize_embeddings(original_embeddings_path, normalized_embeddings_path):
    original_embeddings = load_bin(original_embeddings_path)
    original_embeddings.unit_normalize_all()
    save_bin(original_embeddings, normalized_embeddings_path)
