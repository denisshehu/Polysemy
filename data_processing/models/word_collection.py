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

    @property
    def corpus_path(self):
        return self._corpus_path

    @property
    def embeddings_path(self):
        return self._embeddings_path

    @property
    def senses_path(self):
        return self._senses_path

    def extract(self):
        self._extract_corpus()
        self._extract_embeddings()
        self._extract_senses()

    def _extract_corpus(self):
        tree = load_xml(self._corpus_path)
        root = tree.getroot()
        self._extract_subtree(root)

    def _extract_subtree(self, element):
        if element.tag == 'instance':
            lemma = element.attrib['lemma']
            if lemma in self._words:
                self._words[lemma].increment_count()
            else:
                self._words[lemma] = Word(lemma)

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
            value = sense.split(' ')[1][:-1]
            key = value.split('%')[0]
            sense_counts = self._words[key].sense_counts.copy()
            if value in sense_counts:
                sense_counts[value] += 1
            else:
                sense_counts[value] = 1
            self._words[key].sense_counts = sense_counts

    def save(self):
        save_yaml(self, self._word_collection_path)
