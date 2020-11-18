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
    if not isinstance(text, str):
        return ()

    text = re.sub('[^a-z \n \.]', '', text.lower()).split('.')
    prepared_text = []

    for sentence in text:
        if sentence:
            set_of_words = sentence.split()
            prepared_text.append(tuple(tuple('_' + word + '_') for word in set_of_words))

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
        id_of_letter = self.storage[letter] if (isinstance(letter, str) and letter in self.storage) else -1

        return id_of_letter

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return 1

        for sentence in corpus:
            for word in sentence:
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
    if not isinstance(corpus, tuple) or not corpus or not isinstance(storage, LetterStorage):
        return ()

    new_corpus = []

    for sentence in corpus:
        sentence_list = []
        for word in sentence:
            sentence_list.append(tuple([storage.get_id_by_letter(letter) for letter in word]))
        new_corpus.append(tuple(sentence_list))

    return tuple(new_corpus)


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

        self.n_grams = []
        for sentence in encoded_text:
            for word in sentence:
                self.n_grams.append(tuple(word[idx: idx + self.size] for idx in range(len(word))
                                          if idx < len(word) - self.size + 1))
            self.n_grams = [tuple(self.n_grams)]
        self.n_grams = tuple(self.n_grams)

        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(self.n_grams, tuple) or not self.n_grams:
            return 1

        for sentence in self.n_grams:
            for word in sentence:
                for n_gram in word:
                    if n_gram not in list(self.n_gram_frequencies.keys()):
                        self.n_gram_frequencies[n_gram] = 1
                    else:
                        self.n_gram_frequencies[n_gram] += 1

        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """

        for n_gram in self.n_gram_frequencies:
            appearings = 0
            for differ_n_gram in self.n_gram_frequencies:
                if n_gram[: self.size - 1] == differ_n_gram[: self.size - 1]:
                    appearings += self.n_gram_frequencies[differ_n_gram]
            probability = self.n_gram_frequencies[n_gram] / appearings
            self.n_gram_log_probabilities[n_gram] = math.log(probability)

        if not self.n_gram_log_probabilities:
            return 1

        return 0


    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int) or isinstance(k, bool):
            return ()

        top_n_grams = sorted(self.n_gram_frequencies.keys(), key=self.n_gram_frequencies.get, reverse=True)

        return tuple(top_n_grams[:k])


# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2, 3, 4), top_k: int = 10):
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
        if (not isinstance(encoded_text, tuple) or
            None in encoded_text or
            not isinstance(language_name, str)):

            return 1

        self.n_gram_storages[language_name] = {}
        for n_gram_size in self.trie_levels:
            storage = NGramTrie(n_gram_size)
            storage.fill_n_grams(encoded_text)
            storage.calculate_n_grams_frequencies()
            storage.calculate_log_probabilities()
            self.n_gram_storages[language_name][n_gram_size] = storage

        return 0

    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        if (not isinstance(first_n_grams, tuple) or
            not isinstance(second_n_grams, tuple) or
            None in first_n_grams or
            None in second_n_grams):

            return -1

        distance = 0
        for fst_idx, fst_n_gram in enumerate(first_n_grams):
            if fst_n_gram not in second_n_grams:
                distance += len(second_n_grams)
            for scd_idx, scd_n_gram in enumerate(second_n_grams):
                if fst_n_gram == scd_n_gram:
                    distance += abs(fst_idx - scd_idx)

        return distance


    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        pass

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
