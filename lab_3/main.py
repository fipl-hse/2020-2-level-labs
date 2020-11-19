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
    if not isinstance(text, str):
        return ()

    fin_elems = re.split('[.] ', text)
    tokens = []
    for elems in fin_elems:
        tokenized_text = re.sub('[^a-z \n]', '', elems.lower()).split()
        if not tokenized_text:
            return ()
        tokens.append(tuple(tuple(['_'] + list(i) + ['_']) for i in tokenized_text))

    return tuple(tokens)


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
        store_lngth = len(self.storage)
        if not isinstance(letter, str) or letter == '':
            return 1
        if letter not in self.storage:
            self.storage[letter] = store_lngth + 1
            return 0
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter in self.storage:
            letter_id = self.storage.get(letter)
            return letter_id
        return -1

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return 1

        for sent in corpus:
            for word in sent:
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

    encoded_corpus = []

    for idx1, sentence in enumerate(corpus):
        encoded_corpus.append([])
        for idx2, word in enumerate(sentence):
            encoded_corpus[idx1].append([])
            for letter in word:
                encoded_corpus[idx1][idx2].append(storage.get_id_by_letter(letter))
            encoded_corpus[idx1][idx2] = tuple(encoded_corpus[idx1][idx2])
        encoded_corpus[idx1] = tuple(encoded_corpus[idx1])

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

        self.n_grams = list(self.n_grams)

        n_grams_list = []
        for sentence in encoded_text:
            n_grams_sent = []
            for wrd in sentence:
                n_grams_wrd = []
                for idx in range(len(wrd) - self.size + 1):
                    n_grams_wrd.append(tuple(wrd[idx:idx + self.size]))
                n_grams_sent.append(tuple(n_grams_wrd))
            n_grams_list.append(tuple(n_grams_sent))
        self.n_grams = tuple(n_grams_list)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """

        if not self.n_grams:
            return 1

        for sentence in self.n_grams:
            for wrd in sentence:
                for n_gram in wrd:
                    if n_gram not in self.n_gram_frequencies:
                        self.n_gram_frequencies[n_gram] = 1
                    else:
                        self.n_gram_frequencies[n_gram] += 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """

        if not self.n_gram_frequencies:
            return 1

        for n_gram, freq in self.n_gram_frequencies.items():
            total_n_grams = 0
            for n_gram1 in self.n_gram_frequencies:
                if n_gram1[:-1] == n_gram[:-1]:
                    total_n_grams += self.n_gram_frequencies[n_gram1]
            probability = freq / total_n_grams
            self.n_gram_log_probabilities[n_gram] = log(probability)
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """

        if not isinstance(k, int) or k < 0 or not self.n_gram_frequencies:
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

        type_check = (not isinstance(encoded_text, tuple) or not all(isinstance(i, tuple) for i in encoded_text)
                      or not isinstance(language_name, str))

        if type_check:
            return 1

        self.n_gram_storages[language_name] = {}

        for i in self.trie_levels:
            new_lng = NGramTrie(i)
            new_lng.fill_n_grams(encoded_text)
            new_lng.calculate_n_grams_frequencies()
            new_lng.calculate_log_probabilities()
            self.n_gram_storages[language_name][i] = new_lng

        return 0

    @staticmethod
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        check_1 = ((isinstance(first_n_grams, tuple) and not first_n_grams)
                   or (isinstance(second_n_grams, tuple) and not second_n_grams))

        check_2 = (not isinstance(first_n_grams, tuple) or not isinstance(second_n_grams, tuple) or
                   not all(isinstance(i, tuple) for i in first_n_grams) or
                   not all(isinstance(i, tuple) for i in second_n_grams))

        if check_1:
            return 0

        if check_2:
            return -1

        dist = 0

        for i, n_gram in enumerate(first_n_grams):
            if n_gram in second_n_grams:
                dist += abs(second_n_grams.index(n_gram) - i)
            else:
                dist += len(second_n_grams)

        return dist

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not (isinstance(encoded_text, tuple) and len(encoded_text) and encoded_text[0]
                and len(self.n_gram_storages)):
            return {}

        lng_dict = {}

        for lng, dct in self.n_gram_storages.items():
            dist = 0
            for n_gram_size, n_gram_trie in dct.items():
                top_n_grams = n_gram_trie.top_n_grams(self.top_k)
                unknown_n_gram_trie = NGramTrie(n_gram_size)
                unknown_n_gram_trie.fill_n_grams(encoded_text)
                unknown_n_gram_trie.calculate_n_grams_frequencies()
                top_n_grams1 = unknown_n_gram_trie.top_n_grams(self.top_k)
                dist += self._calculate_distance(top_n_grams, top_n_grams1)
            lng_dict[lng] = dist / len(dct)

        return lng_dict


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
