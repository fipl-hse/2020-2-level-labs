"""
Language detection using n-grams
"""

import re
from math import log

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
    if not isinstance(text, str) or text == 0:
        return ()

    sentences = re.split('[!?.]', text)
    letter_list = []

    for sentence in sentences:
        token_list = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if not token_list:
            continue
        letter_list.append(tuple(tuple(['_'] + list(token) + ['_']) for token in token_list))
    return tuple(letter_list)


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
        if not isinstance(letter, str) or not len(letter) <= 1:
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

    corpus_encode = []
    for sentence in corpus:
        sentence_list = []
        for token in sentence:
            sentence_list.append(tuple([storage.get_id_by_letter(letter) for letter in token]))
        corpus_encode.append(tuple(sentence_list))

    return tuple(corpus_encode)


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
        check = isinstance(encoded_text, tuple)
        if not check:
            return 1

        n_grams_list = []
        for sentences in encoded_text:
            n_grams_sent = []
            for token in sentences:
                n_grams_token = []
                for index in range(len(token) - self.size + 1):
                    n_grams_token.append(tuple(token[index:index + self.size]))
                n_grams_sent.append(tuple(n_grams_token))
            n_grams_list.append(tuple(n_grams_sent))
        self.n_grams = tuple(n_grams_list)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if len(self.n_grams) == 0:
            return 1

        for sentence in self.n_grams:
            for word in sentence:
                for n_gram in word:
                    self.n_gram_frequencies[n_gram] = self.n_gram_frequencies.get(n_gram, 0) + 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if len(self.n_gram_frequencies) == 0:
            return 1

        for n_gram in self.n_gram_frequencies:
            probable = self.n_gram_frequencies[n_gram] / \
                       sum([self.n_gram_frequencies[n_gram_other]
                            for n_gram_other in self.n_gram_frequencies
                            if n_gram[:self.size - 1] == n_gram_other[:self.size - 1]])
            self.n_gram_log_probabilities[n_gram] = log(probable)
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int) or k < 0 or len(self.n_gram_frequencies) == 0:
            return ()
        return tuple(sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)[:k])


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
        if not isinstance(encoded_text, tuple) or None in encoded_text or not isinstance(language_name, str):
            return 1

        self.n_gram_storages[language_name] = {}
        for trie_level in self.trie_levels:
            language_storage = NGramTrie(trie_level)
            language_storage.fill_n_grams(encoded_text)
            language_storage.calculate_n_grams_frequencies()
            language_storage.calculate_log_probabilities()
            self.n_gram_storages[language_name][trie_level] = language_storage
        return 0

    @staticmethod
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        incorrect_inputs = (not isinstance(first_n_grams, tuple) or
                            not isinstance(second_n_grams, tuple) or
                            None in first_n_grams or None in second_n_grams)
        if incorrect_inputs:
            return -1

        total_dist = 0
        for ind, n_gram in enumerate(first_n_grams):
            if n_gram in second_n_grams:
                total_dist += abs(second_n_grams.index(n_gram) - ind)
            else:
                total_dist += len(second_n_grams)
        return total_dist

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple) or encoded_text == 0 or self.n_gram_storages == {}:
            return {}

        lang_dict = {}
        for language_name, language_storage in self.n_gram_storages.items():
            lang_dict[language_name] = []
            for trie_level, n_gram_trie in language_storage.items():
                storage_text = NGramTrie(trie_level)
                storage_text.fill_n_grams(encoded_text)
                storage_text.calculate_n_grams_frequencies()
                lang_dict[language_name].append(self._calculate_distance(n_gram_trie.top_n_grams(self.top_k),
                                                                         storage_text.top_n_grams(self.top_k)))
            lang_dict[language_name] = sum(lang_dict[language_name]) / len(lang_dict[language_name])
        return lang_dict


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
