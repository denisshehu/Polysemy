from data_processing.data_storage import *


def fix_sco_corpus():
    data = load_txt(sco_corpus_path)
    data.insert(1, '<root>\n')
    data.append('</root>\n')
    save_txt(data, fixed_sco_corpus_path)
