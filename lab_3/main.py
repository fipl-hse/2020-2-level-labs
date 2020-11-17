"""
Language detection using n-grams
"""
import re
import math


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

    sentences = re.split('[.!?] ', text)
    prepared_text = []

    for sentence in sentences:
        list_words = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if not len(list_words):
            continue
        prepared_text.append(tuple(tuple(['_'] + list(word) + ['_']) for word in list_words))

    return tuple(prepared_text)


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
        if not isinstance(letter, str) or not letter:
            return 1

        if letter not in self.storage:
            self.storage[letter] = len(self.storage) + 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) or letter not in self.storage or not 0 < len(letter) <= 1:
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

        for word in corpus:
            for letter in word:
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

    encoded_corp = []
    for sentence in corpus:
        list_sentence = []
        for token in sentence:
            list_sentence.append(tuple([storage.get_id_by_letter(letter) for letter in token]))
        encoded_corp.append(tuple(list_sentence))

    return tuple(encoded_corp)


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
        for sentence in encoded_text:
            n_grams_sentence = []
            for token in sentence:
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
        if not self.n_gram_frequencies:
            return 1

        for pair in self.n_gram_frequencies:
            appearing = 0
            for begin in self.n_gram_frequencies:
                if pair[0] in begin:
                    appearing += self.n_gram_frequencies[begin]
            self.n_gram_log_probabilities[pair] = math.log(self.n_gram_frequencies[pair] / appearing)
        if not self.n_gram_log_probabilities:
            return 1

        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if len(self.n_gram_frequencies) == 0:
            return 1

        for n_gram, frequency in self.n_gram_frequencies.items():
            probability = frequency / sum([self.n_gram_frequencies[n_gram1] for n_gram1 in self.n_gram_frequencies if
                                           n_gram1[:-1] == n_gram[:-1]])
            self.n_gram_log_probabilities[n_gram] = math.log(probability)

        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int) or len(self.n_gram_frequencies) == 0:
            return ()

        most_common = sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)[:k]

        return tuple(most_common)


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
        if (not isinstance(encoded_text, tuple) or not all(isinstance(i, tuple) for i in encoded_text)
                or not isinstance(language_name, str)):
            return 1

        self.n_gram_storages[language_name] = {}

        for trie_level in self.trie_levels:
            storage_lang = NGramTrie(trie_level)
            storage_lang.fill_n_grams(encoded_text)
            storage_lang.calculate_n_grams_frequencies()
            storage_lang.calculate_log_probabilities()
            self.n_gram_storages[language_name][trie_level] = storage_lang

        return 0

    @staticmethod
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        if ((isinstance(first_n_grams, tuple) and not first_n_grams) or
                (isinstance(second_n_grams, tuple) and not second_n_grams)):
            return 0

        if (not isinstance(first_n_grams, tuple) or not isinstance(second_n_grams, tuple)
                or not all(isinstance(i, tuple) for i in first_n_grams)
                or not all(isinstance(i, tuple) for i in second_n_grams)):
            return -1

        distance = 0

        for ind, n_gram in enumerate(first_n_grams):
            if n_gram in second_n_grams:
                distance += abs(second_n_grams.index(n_gram) - ind)
            else:
                distance += len(second_n_grams)

        return distance

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple) or not all(encoded_text):
            return {}

        distance_lang = {}
        for language_name, storage_lang in self.n_gram_storages.items():
            distance_lang[language_name] = []
            for trie_level, n_gram_trie in storage_lang.items():
                text_storage = NGramTrie(trie_level)
                text_storage.fill_n_grams(encoded_text)
                text_storage.calculate_n_grams_frequencies()
                distance_lang[language_name].append(
                    self._calculate_distance(n_gram_trie.top_n_grams(self.top_k),
                                             text_storage.top_n_grams(self.top_k)))

            distance_lang[language_name] = sum(distance_lang[language_name]) / len(distance_lang[language_name])

        return distance_lang


# 10
class ProbabilityLanguageDetector(LanguageDetector):

    def _calculate_sentence_probability(self, n_gram_storage: NGramTrie, sentence_n_grams: tuple) -> float:
        """
        Calculates sentence probability
        :param n_gram_storage: a filled NGramTrie with log-probabilities
        :param sentence_n_grams: n-grams from a sentence
        :return: a probability of a sentence
        """
        return 0

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        return {}
