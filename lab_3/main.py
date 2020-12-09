"""
Language detection using n-grams
"""


import re
from math import log
from statistics import mean




# 4
def tokenize_by_sentence(text: str) -> tuple:
    """
    Splits a text into sentences, sentences into tokens, tokens into letters
    Tokens are framed with '_'
    :param text: a text
    :return: a tuple of sentence with tuples of tokens split into letters
    e.g.
    text = 'She is happy. He is happy.'
    -->  (
         (('_', 's', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_')),
         (('_', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_'))
         )
    """
    if not isinstance(text, str) or len(text) == 0:
        return ()
    sentences = re.split('[!?.] ', text)
    list_letters = []

    for sentence in sentences:
        list_tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if not list_tokens:
            continue
        list_letters.append(tuple(tuple(['_'] + list(token) + ['_']) for token in list_tokens))


    return tuple(list_letters)


# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str) or letter == '':
            return 1
        if letter not in self.storage:
            self.storage[letter] = 1 + len(self.storage)
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) or letter not in self.storage or letter == '':
            return -1
        return self.storage[letter]

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return 1
        for sentence in corpus:
            for token in sentence:
                for letter in token:
                    self._put_letter(letter)
        return 0


# 6
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()
    encoded_corpus = []
    for element in corpus:
        list_element = []
        for word in element:
            list_element.append(tuple([storage.get_id_by_letter(letter) for letter in word]))
        encoded_corpus.append(tuple(list_element))
    return tuple(encoded_corpus)


# 6
class NGramTrie:

    def __init__(self, n: int):
        self.size = n
        self.n_grams = ()
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

    def fill_n_grams(self, encoded_text: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(encoded_text, tuple):
            return 1
        list_n_grams = []
        for element in encoded_text:
            n_grams_sentence = []
            for token in element:
                n_grams_token = []
                for ind in range(len(token) - self.size + 1):
                    n_grams_token.append(tuple(token[ind:ind + self.size]))
                n_grams_sentence.append(tuple(n_grams_token))
            list_n_grams.append(tuple(n_grams_sentence))
        self.n_grams = tuple(list_n_grams)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_grams:
            return 1
        for element in self.n_grams:
            for token in element:
                for n_gram in token:
                    self.n_gram_frequencies[n_gram] = self.n_gram_frequencies.get(n_gram, 0) + 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1
        for element in self.n_gram_frequencies:
            probab = self.n_gram_frequencies[element] / sum([self.n_gram_frequencies[n_gram]
                                                             for n_gram in self.n_gram_frequencies
                                                             if n_gram[0] == element[0]])
            self.n_gram_log_probabilities[element] = log(probab)
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int) or k < 0:
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
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(encoded_text, tuple) or not isinstance(encoded_text[0], tuple)\
                or not isinstance(language_name, str):
            return 1

        self.n_gram_storages[language_name] = {}
        for element in self.trie_levels:
            storage_language = NGramTrie(element)
            storage_language.fill_n_grams(encoded_text)
            storage_language.calculate_n_grams_frequencies()
            storage_language.calculate_log_probabilities()
            self.n_gram_storages[language_name][element] = storage_language
        return 0

    @staticmethod

    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        if not isinstance(first_n_grams, tuple) or not isinstance(second_n_grams, tuple):
            return -1
        if (first_n_grams and not isinstance(first_n_grams[0], (tuple, str))) \
                or (second_n_grams and not isinstance(second_n_grams[0], (tuple, str))):
            return -1
        distance = 0
        for index_1, n_gam in enumerate(first_n_grams):
            if n_gam in second_n_grams:
                distance += abs(second_n_grams.index(n_gam) - index_1)
            else:
                distance += len(second_n_grams)
        return distance

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple):
            return {}
        detect_language_dict = {}
        for language in self.n_gram_storages:
            language_dis = []
            for size in self.trie_levels:
                unknown_n_gram = NGramTrie(size)
                unknown_n_gram.fill_n_grams(encoded_text)
                unknown_n_gram.calculate_n_grams_frequencies()
                top_unknown_n_gram = unknown_n_gram.top_n_grams(self.top_k)
                top_language = self.n_gram_storages[language][size].top_n_grams(self.top_k)
                language_dis.append(self._calculate_distance(top_unknown_n_gram, top_language))
            if language_dis:
                detect_language_dict[language] = mean(language_dis)
        return detect_language_dict


# 10
class ProbabilityLanguageDetector(LanguageDetector):

    def _calculate_sentence_probability(self, n_gram_storage: NGramTrie, sentence_n_grams: tuple) -> float:
        """
        Calculates sentence probability
        :param n_gram_storage: a filled NGramTrie with log-probabilities
        :param sentence_n_grams: n-grams from a sentence
        :return: a probability of a sentence
        """
        pass

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        pass
