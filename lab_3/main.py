"""
Language detection using n-grams
"""
import re
from math import log
from statistics import mean


# 4
def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        return ()
    result = []
    sentences = re.split('[.!?] ', text)
    for sentence in sentences:
        letters_token = []
        tokens = re.sub('[^a-z \n]', '', sentence.lower())
        tokens = tokens.split()
        for token in tokens:
            letters_token.append(tuple(['_'] + list(token) + ['_']))
        if letters_token:
            result.append(tuple(letters_token))
    return tuple(result)

# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}

    def _put_letter(self, letter: str) -> int:
        if not isinstance(letter, str) or not 0 < len(letter) <= 1:
            return 1
        if letter not in self.storage:
            self.storage[letter] = len(self.storage)
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        checks = [not isinstance(letter, str)
                  or letter not in self.storage
                  or not len(letter) > 0]
        if all(checks):
            return -1
        return self.storage[letter]

    def update(self, corpus: tuple) -> int:
        if not isinstance(corpus, tuple):
            return 1
        for sentence in corpus:
            for token in sentence:
                for letter in token:
                    self._put_letter(letter)
        return 0


# 6
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()
    encoded_corpus = []
    for sentence in corpus:
        encoded_token = []
        for token in sentence:
            encoded_token.append(tuple([storage.get_id_by_letter(letter) for letter in token]))
        encoded_corpus.append(tuple(encoded_token))
    return tuple(encoded_corpus)


# 6
class NGramTrie:

    def __init__(self, n: int):
        self.size = n
        self.n_grams = ()
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

    def fill_n_grams(self, encoded_text: tuple) -> int:
        if not isinstance(encoded_text, tuple):
            return 1
        self.n_grams = []
        for sentence in encoded_text:
            sentence_n_grams = []
            for token in sentence:
                token_n_grams = []
                for index in range(len(token) - self.size + 1):
                    n_grams = token[index:index+self.size]
                    token_n_grams.append(n_grams)
                sentence_n_grams.append(tuple(token_n_grams))
            self.n_grams.append(tuple(sentence_n_grams))
        self.n_grams = tuple(self.n_grams)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        for sentence in self.n_grams:
            for token in sentence:
                for n_gram in token:
                    self.n_gram_frequencies[n_gram] = self.n_gram_frequencies.get(n_gram, 0) + 1
        if not self.n_gram_frequencies:
            return 1
        return 0

    def calculate_log_probabilities(self) -> int:
        for n_gram in self.n_gram_frequencies:
            sum_n_grams = [self.n_gram_frequencies[l_gram] for l_gram in self.n_gram_frequencies
                           if l_gram[0] == n_gram[0]]
            self.n_gram_log_probabilities[n_gram] = log(self.n_gram_frequencies[n_gram] / sum(sum_n_grams))
        if not self.n_gram_log_probabilities:
            return 1
        return 0

    def top_n_grams(self, k: int) -> tuple:
        if not isinstance(k, int):
            return ()
        top = sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)
        return tuple(top[:k])


# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2,), top_k: int = 10):
        self.trie_levels = trie_levels
        self.top_k = top_k
        self.n_gram_storages = {}

    def new_language(self, encoded_text: tuple, language_name: str) -> int:
        checks = [not isinstance(encoded_text, tuple)
                  or not isinstance(language_name, str)
                  or None in encoded_text]
        if all(checks):
            return 1
        self.n_gram_storages[language_name] = {}
        for trie_level in self.trie_levels:
            trie = NGramTrie(trie_level)
            trie.fill_n_grams(encoded_text)
            trie.calculate_n_grams_frequencies()
            trie.calculate_log_probabilities()
            self.n_gram_storages[language_name].update({trie_level: trie})
        return 0

    @staticmethod
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        if not isinstance(first_n_grams, tuple) or not isinstance(second_n_grams, tuple) or \
                None in first_n_grams or None in second_n_grams:
            return -1
        distance = []
        for first_index, first_n_gram in enumerate(first_n_grams):
            if first_n_gram not in second_n_grams:
                distance.append(len(second_n_grams))
            for second_index, second_n_gram in enumerate(second_n_grams):
                if first_n_gram == second_n_gram:
                    distance.append(abs(first_index - second_index))
        return sum(distance)

    def detect_language(self, encoded_text: tuple) -> dict:
        if not isinstance(encoded_text, tuple) or None in encoded_text or \
                encoded_text == () or self.n_gram_storages == {}:
            return {}
        detected = {}
        for language in self.n_gram_storages:
            language_distance = []
            for size in self.trie_levels:
                storage = NGramTrie(size)
                storage.fill_n_grams(encoded_text)
                storage.calculate_n_grams_frequencies()
                top_storage = storage.top_n_grams(self.top_k)
                top_language = self.n_gram_storages[language][size].top_n_grams(self.top_k)
                language_distance.append(self._calculate_distance(top_storage, top_language))
            if language_distance:
                detected[language] = mean(language_distance)
        return detected


# 10
class ProbabilityLanguageDetector(LanguageDetector):

    def _calculate_sentence_probability(self, n_gram_storage: NGramTrie, sentence_n_grams: tuple) -> float:
        pass

    def detect_language(self, encoded_text: tuple) -> dict:
        pass
