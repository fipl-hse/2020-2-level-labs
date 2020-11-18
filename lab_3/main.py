"""
Language detection using n-grams
"""
import re
import math
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
    if not isinstance(text, str):
        return ()
    tokens = []
    sentences = text.split('.')
    for sentence in sentences:
        letters_sentence = []
        token_sentence = re.sub('[^a-z \n]', '', sentence.lower()).split()
        for token in token_sentence:
            letters_sentence.append(tuple(['_'] + list(token) + ['_']))
        if letters_sentence:
            tokens.append(tuple(letters_sentence))
    return tuple(tokens)

# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}
        self.ids = 0

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str) or letter == '':
            return 1
        if letter not in self.storage:
            self.storage[letter] = self.ids
            self.ids += 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter not in self.storage:
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
    if not isinstance(corpus, tuple) or not isinstance(storage, LetterStorage):
        return ()
    encoded_corpus = []
    for sentence in corpus:
        encoded_sentence = []
        for token in sentence:
            encoded_token = []
            for letter in token:
                encoded_token.append(storage.get_id_by_letter(letter))
            encoded_sentence.append(tuple(encoded_token))
        encoded_corpus.append(tuple(encoded_sentence))
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
        text_of_n_grams = []
        for sentence in encoded_text:
            sentence_of_n_grams = []
            for token in sentence:
                token_of_n_grams = []
                for index in range(len(token)):
                    if index != len(token) - (self.size - 1):
                        n_grams = token[index:self.size + index]
                        if len(n_grams) == self.size:
                            token_of_n_grams.append(n_grams)
                if token_of_n_grams:
                    sentence_of_n_grams.append(tuple(token_of_n_grams))
            text_of_n_grams.append(tuple(sentence_of_n_grams))
        self.n_grams = tuple(text_of_n_grams)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        for sentence in self.n_grams:
            for token in sentence:
                for element in token:
                    self.n_gram_frequencies[element] = self.n_gram_frequencies.get(element, 0) + 1
        if not self.n_gram_frequencies:
            return 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        for pair in self.n_gram_frequencies:
            appearing = 0
            for begin in self.n_gram_frequencies:
                if pair[0] in begin:
                    appearing += self.n_gram_frequencies[begin]
            self.n_gram_log_probabilities[pair] = math.log(self.n_gram_frequencies[pair] / appearing)
        if not self.n_gram_log_probabilities:
            return 1
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int):
            return ()
        top = sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)
        return tuple(top[:k])


# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2, 3, 5), top_k: int = 10):
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
        for size in self.trie_levels:
            self.n_gram_storages[language_name].update({size: NGramTrie(size)})
            trie = self.n_gram_storages[language_name][size]
            trie.fill_n_grams(encoded_text)
            trie.calculate_n_grams_frequencies()
            trie.calculate_log_probabilities()
        return 0

    @staticmethod
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
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
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple) or None in encoded_text or \
                encoded_text == () or self.n_gram_storages == {}:
            return {}
        dis_dict = {}
        for language in self.n_gram_storages:
            language_distance = []
            for size in self.trie_levels:
                unknown = NGramTrie(size)
                unknown.fill_n_grams(encoded_text)
                unknown.calculate_n_grams_frequencies()
                top_unknown = unknown.top_n_grams(self.top_k)
                top_language = self.n_gram_storages[language][size].top_n_grams(self.top_k)
                language_distance.append(self._calculate_distance(top_unknown, top_language))
            if language_distance:
                dis_dict[language] = mean(language_distance)
        return dis_dict


# 10
class ProbabilityLanguageDetector(LanguageDetector):

    @staticmethod
    def _calculate_sentence_probability(n_gram_storage: NGramTrie, sentence_n_grams: tuple) -> float:
        """
        Calculates sentence probability
        :param n_gram_storage: a filled NGramTrie with log-probabilities
        :param sentence_n_grams: n-grams from a sentence
        :return: a probability of a sentence
        """
        if not isinstance(n_gram_storage, NGramTrie) or not isinstance(sentence_n_grams, tuple):
            return -1.0
        log_probabilities = []
        for n_gram_sentence in sentence_n_grams:
            for n_gram in n_gram_sentence:
                for one_n_gram in n_gram:
                    if one_n_gram in n_gram_storage.n_gram_log_probabilities:
                        log_probabilities.append(n_gram_storage.n_gram_log_probabilities[one_n_gram])
        return sum(log_probabilities)


    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        if not isinstance(encoded_text, tuple) or None in encoded_text:
            return {}
        prob_dict = {}
        for language in self.n_gram_storages:
            language_probability = []
            for size in self.trie_levels:
                language_probability.append(self._calculate_sentence_probability(self.n_gram_storages[language][size],
                                                                                 encoded_text))
            if language_probability:
                prob_dict[language] = mean(language_probability)
        return prob_dict
