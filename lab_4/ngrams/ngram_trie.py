"""
N-gram model
"""
from math import log


class NGramTrie:
    def __init__(self, n_gram_size: int, encoded_text: tuple):
        self.size = n_gram_size
        self.encoded_text = encoded_text
        self.n_grams = ()
        self.n_gram_frequencies = {}
        self.uni_grams = {}
        self._fill_n_grams()
        self._calculate_n_grams_frequencies()

    def _fill_n_grams(self):

        if not isinstance(self.encoded_text, tuple):
            raise ValueError

        n_grams = []
        for i in range(len(self.encoded_text) - self.size + 1):
            n_grams.append(tuple(self.encoded_text[i:i + self.size]))
        self.n_grams = tuple(n_grams)

        for word in self.encoded_text:
            if (word, ) not in self.uni_grams:
                self.uni_grams[(word, )] = self.encoded_text.count(word)

    def _calculate_n_grams_frequencies(self):

        for n_gram in self.n_grams:
            if n_gram in self.n_gram_frequencies:
                self.n_gram_frequencies[n_gram] += 1
            else:
                self.n_gram_frequencies[n_gram] = 1

    def top_n_grams(self, k: int) -> tuple:

        if not isinstance(k, int) or k < 0 or not self.n_gram_frequencies:
            return ()
        return tuple(sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)[:k])

    def calculate_probabilities(self) -> int:
        if not self.n_gram_frequencies:
            return 1

        for n_gram in self.n_gram_frequencies:
            probability = self.n_gram_frequencies[n_gram] / \
                          sum([self.n_gram_frequencies[other_n_gram]
                               for other_n_gram in self.n_gram_frequencies
                               if n_gram[:self.size - 1] == other_n_gram[:self.size - 1]])
        return probability
