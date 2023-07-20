from utils import *


class Word:

    def __init__(self, value, pos):
        self._value = value
        self._count = None
        self._pos_counts = {pos: 1}
        self._sense_counts = dict()
        self._n_senses = None
        self._n_total_senses = None
        self._embedding = None

    @property
    def value(self):
        return self._value

    @property
    def count(self):
        return self._count

    @property
    def pos_counts(self):
        return self._pos_counts

    @property
    def sense_counts(self):
        return self._sense_counts

    @property
    def n_senses(self):
        return self._n_senses

    @property
    def n_total_senses(self):
        return self._n_total_senses

    @property
    def embedding(self):
        return self._embedding

    @embedding.setter
    def embedding(self, embedding):
        self._embedding = embedding

    def update_pos_counts(self, pos):
        if pos in self._pos_counts:
            self._pos_counts[pos] += 1
        else:
            self._pos_counts[pos] = 1

    def update_sense_counts(self, sense):
        if sense in self._sense_counts:
            self._sense_counts[sense] += 1
        else:
            self._sense_counts[sense] = 1

    def set_count(self):
        self._count = sum(self._pos_counts.values())

    def set_n_senses(self):
        self._n_senses = len(self._sense_counts)

    def set_n_total_senses(self):
        n_total_senses = 0
        for pos in self._pos_counts:
            n_total_senses += len(wn.synsets(self._value, getattr(wn, pos)))
        self._n_total_senses = n_total_senses
