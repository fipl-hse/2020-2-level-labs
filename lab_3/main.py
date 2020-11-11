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
    if not isinstance(text, str) or len(text) == 0:
        return ()

    sentences = re.split('[.!?] ', text)
    output = []
    for sentence in sentences:
        list_words = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if len(list_words) == 0:
            continue
        output.append(tuple(tuple(['_'] + list(word) + ['_']) for word in list_words))

    return tuple(output)


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
        if not isinstance(letter, str) or not 0 < len(letter) <= 1:
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
                if isinstance(letter, tuple):
                    for symbol in letter:
                        self._put_letter(symbol)
                else:
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
    for sentence in corpus:
        if isinstance(sentence[0], tuple):
            sentence_list = []
            for word in sentence:
                sentence_list.append(tuple([storage.get_id_by_letter(letter) for letter in word]))
            encoded_corpus.append(tuple(sentence_list))
        else:
            encoded_corpus.append(tuple([storage.get_id_by_letter(letter) for letter in sentence]))

    if len(encoded_corpus) == 0:
        return tuple(encoded_corpus)
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
        self.n_grams = []
        for sentence in encoded_text:
            tuple_sentence = []
            for word in sentence:
                tuple_word = []
                for ind in range(len(word) - self.size + 1):
                    tuple_word.append(tuple(word[ind:ind+self.size]))
                tuple_sentence.append(tuple(tuple_word))
            self.n_grams.append(tuple(tuple_sentence))
        self.n_grams = tuple(self.n_grams)
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
            probability = self.n_gram_frequencies[n_gram] / \
                          sum([self.n_gram_frequencies[gram]
                               for gram in self.n_gram_frequencies
                               if gram[0] == n_gram[0]])
            self.n_gram_log_probabilities[n_gram] = log(probability)
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int) or k < 1 or len(self.n_gram_frequencies) == 0:
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
        if not isinstance(encoded_text, tuple) or not isinstance(encoded_text[0], tuple) \
                or not isinstance(language_name, str):
            return 1
        self.n_gram_storages[language_name] = {}
        for level in self.trie_levels:
            storage_language = NGramTrie(level)
            storage_language.fill_n_grams(encoded_text)
            storage_language.calculate_n_grams_frequencies()
            storage_language.calculate_log_probabilities()
            self.n_gram_storages[language_name][level] = storage_language
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
        if len(first_n_grams) != 0 and not (isinstance(first_n_grams[0], tuple) or isinstance(first_n_grams[0], str)):
            return -1
        if len(second_n_grams) != 0 and not (isinstance(second_n_grams[0], tuple) or isinstance(second_n_grams[0], str)):
            return -1

        #if (len(first_n_grams) == 0 and len(second_n_grams) > 0) or\
          #     (len(second_n_grams) == 0 and len(first_n_grams) > 0):
           # return 0
        sum_distance = 0
        list_all_first = []
        list_all_second = []
        try:
            if isinstance(first_n_grams[0][0], int):
                list_all_first = first_n_grams
                list_all_second = second_n_grams
            else:
                for sentence in first_n_grams:
                    if isinstance(sentence[0], int):
                        list_all_first.append(sentence)
                    else:
                        for word in sentence:
                            list_all_first.extend(list(word))
                for sentence in second_n_grams:
                    if isinstance(sentence[0], int):
                        list_all_second.append(sentence)
                    else:
                        for word in sentence:
                            list_all_second.extend(list(word))
        except IndexError:
            return 0

        for ind, gram in enumerate(list_all_first):
            if gram in list_all_second:
                sum_distance += abs(list_all_second.index(gram) - ind)
            else:
                sum_distance += len(list_all_second)

        return sum_distance

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple):
            return {}
        languages_dist = {}

        for name, language in self.n_gram_storages.items():
            languages_dist[name] = []
            for level_int, level in language.items():
                top_grams = level.top_n_grams(self.top_k)
                storage_language = NGramTrie(level_int)
                storage_language.fill_n_grams(encoded_text)
                storage_language.calculate_n_grams_frequencies()
                languages_dist[name].append(
                    LanguageDetector._calculate_distance(top_grams, storage_language.top_n_grams(self.top_k))
                )
            languages_dist[name] = sum(languages_dist[name]) / len(languages_dist[name])

        return languages_dist


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
