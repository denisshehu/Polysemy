class Word:

    def __init__(self, value):
        self._value = value
        self._count = 1
        self._embedding = None
        self._sense_counts = dict()

    @property
    def value(self):
        return self._value

    @property
    def count(self):
        return self._count

    @property
    def embedding(self):
        return self._embedding

    @embedding.setter
    def embedding(self, embedding):
        self._embedding = embedding

    @property
    def sense_counts(self):
        return self._sense_counts

    @sense_counts.setter
    def sense_counts(self, sense_counts):
        self._sense_counts = sense_counts

    def increment_count(self):
        self._count += 1
