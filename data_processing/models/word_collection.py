from data_processing.models.word import *
from data_processing.data_storage import *


class WordCollection:

    def __init__(self, paths):
        corpus_path, embeddings_path, senses_path, word_collection_path = paths
        self._words = dict()
        self._corpus_path = corpus_path
        self._embeddings_path = embeddings_path
        self._senses_path = senses_path
        self._word_collection_path = word_collection_path

    @property
    def words(self):
        return self._words

    def extract(self):
        self._extract_corpus()
        self._extract_embeddings()
        self._extract_senses()
        self._extra()

    def _extract_corpus(self):
        tree = load_xml(self._corpus_path)
        root = tree.getroot()
        self._extract_subtree(root)

    def _extract_subtree(self, element):
        if element.tag == 'instance':
            lemma = element.attrib['lemma']
            pos = element.attrib['pos']
            if lemma in self._words:
                self._words[lemma].update_pos_counts(pos)
            else:
                self._words[lemma] = Word(lemma, pos)

        for child in element:
            self._extract_subtree(child)

    def _extract_embeddings(self):
        embeddings = load_bin(self._embeddings_path)

        for key in self._words.keys():
            try:
                self._words[key].embedding = embeddings[key]
            except:
                pass

    def _extract_senses(self):
        senses = load_txt(self._senses_path)

        for sense in senses:
            values = sense.split(' ')[1:]
            for value in values:
                value = value.replace('\n', '')
                key = value.split('%')[0]
                self._words[key].update_sense_counts(value)

    def _extra(self):
        for word in self._words.values():
            word.set_count()
            word.set_n_senses()
            word.set_n_total_senses()

    def save(self):
        save_yaml(self, self._word_collection_path)
