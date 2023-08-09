from data_processing.models.word import *
from data_processing.data_storage import *


class WordCollection:

    def __init__(self, corpus_path, embeddings_path, senses_path, word_collection_path, words=None):
        self._words = dict() if words is None else words
        self._corpus_path = corpus_path
        self._embeddings_path = embeddings_path
        self._senses_path = senses_path
        self._word_collection_path = word_collection_path

        if words is None:
            self._extract()
            if self._word_collection_path is not None:
                self._save()

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, words):
        self._words = words

    def _extract(self):
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

    def _save(self):
        save_yaml(self, self._word_collection_path)

    def filter_by_membership(self, attribute, values_list, negate=False):
        words = dict()

        for word in self._words.values():
            value = getattr(word, attribute)
            if values_list == [None]:
                if (not negate and value is None) or (negate and value is not None):
                    words[word.value] = word
            else:
                if (not negate and value in values_list) or (negate and value not in values_list):
                    words[word.value] = word

        return WordCollection(self._corpus_path, self._embeddings_path, self._senses_path, self._word_collection_path,
                              words)

    def filter_by_range(self, attribute, min_value=None, max_value=None):
        words = dict()

        for word in self._words.values():
            value = getattr(word, attribute)

            if None not in (min_value, max_value):
                if min_value <= value <= max_value:
                    words[word.value] = word
            elif min_value is not None:
                if value >= min_value:
                    words[word.value] = word
            elif max_value is not None:
                if value <= max_value:
                    words[word.value] = word

        return WordCollection(self._corpus_path, self._embeddings_path, self._senses_path, self._word_collection_path,
                              words)

    def get_words_with_embedding(self):
        words_with_embedding = self.filter_by_membership('embedding', [None], True)
        return words_with_embedding

    def get_monosemes(self, n=None, use_n_total_senses=True):
        words_with_embedding = self.get_words_with_embedding()
        attribute = 'n_total_senses' if use_n_total_senses else 'n_senses'
        monosemes = words_with_embedding.filter_by_range(attribute, max_value=1)
        if n is not None:
            monosemes.words = dict(sorted(monosemes.words.items(), key=lambda item: item[1].count, reverse=True)[:n])
        return monosemes

    def get_polysemes(self, n=None, use_n_total_senses=True):
        words_with_embedding = self.get_words_with_embedding()
        attribute = 'n_total_senses' if use_n_total_senses else 'n_senses'
        polysemes = words_with_embedding.filter_by_range(attribute, min_value=2)
        if n is not None:
            polysemes.words = dict(sorted(
                polysemes.words.items(), key=lambda item: getattr(item[1], attribute), reverse=True)[:n])
        return polysemes
