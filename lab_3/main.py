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

    sentences = re.split(r'[.!?] ', text)
    result = []

    for sentence in sentences:
        words = re.sub(r'[^a-z \n]', '', sentence.lower()).split()
        if len(words) == 0:
            return ()
        result.append(tuple(tuple(['_'] + list(word) + ['_']) for word in words))

    return tuple(result)


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
        if not isinstance(letter, str):
            return 1

        if letter not in self.storage:
            self.storage[letter] = len(self.storage)

        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) or letter not in self.storage:
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
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()

    encoded_corpus = []

    for sentence in corpus:
        sentences = []

        for word in sentence:
            sentences.append(tuple([storage.get_id_by_letter(letter) for letter in word]))

        encoded_corpus.append(tuple(sentences))

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
            sentence_grams = []

            for word in sentence:
                word_grams = []

                for i in range(len(word) - self.size + 1):
                    word_grams.append(tuple(word[i:i + self.size]))

                sentence_grams.append(tuple(word_grams))

            self.n_grams.append(tuple(sentence_grams))

        self.n_grams = tuple(self.n_grams)

        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_grams:
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
        if not self.n_gram_frequencies:
            return 1

        for n_gram in self.n_gram_frequencies:
            sum_frequencies = sum([self.n_gram_frequencies[gram] for gram in self.n_gram_frequencies
                                   if gram[:-1] == n_gram[:-1]])
            probability = self.n_gram_frequencies[n_gram] / sum_frequencies

            self.n_gram_log_probabilities[n_gram] = math.log(probability)

        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int):
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

        self.n_gram_storages[language_name] = {i: NGramTrie(i) for i in self.trie_levels}

        for i in self.trie_levels:

            self.n_gram_storages[language_name][i].fill_n_grams(encoded_text)

        return 0

    @staticmethod
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """

        if not isinstance(first_n_grams, tuple) or not isinstance(second_n_grams, tuple)\
                or None in first_n_grams or None in second_n_grams:
            return -1

        if not first_n_grams or not second_n_grams:
            return 0

        distance = 0

        for i, gram in enumerate(first_n_grams):
            if gram in second_n_grams:
                distance += abs(second_n_grams.index(gram) - i)
            else:
                distance += len(second_n_grams)

        return distance

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """

        if not (isinstance(encoded_text, tuple) and len(encoded_text) and encoded_text[0]
                and len(self.n_gram_storages)):
            return {}

        languages_dict = {}
        for language in self.n_gram_storages:
            languages_dict[language] = []
            for i in self.trie_levels:
                storage = NGramTrie(i)
                storage.fill_n_grams(encoded_text)
                storage.calculate_n_grams_frequencies()

                self.n_gram_storages[language][i].calculate_n_grams_frequencies()

                languages_dict[language].append(self._calculate_distance(storage.top_n_grams(self.top_k),
                                                self.n_gram_storages[language][i].top_n_grams(self.top_k)))

            languages_dict[language] = sum(languages_dict[language]) / len(languages_dict[language])

        return languages_dict


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
        if not isinstance(sentence_n_grams, tuple) or not isinstance(n_gram_storage, NGramTrie):
            return -1.0

        n_gram_storage.calculate_n_grams_frequencies()
        n_gram_storage.calculate_log_probabilities()

        sentence_probability = 0
        for sentence in sentence_n_grams:
            for word in sentence:
                for n_gram in word:
                    sentence_probability += n_gram_storage.n_gram_log_probabilities.get(n_gram, 0)

        return sentence_probability

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        if not isinstance(encoded_text, tuple):
            return {}

        prob_dict = {}

        for language_name in self.n_gram_storages:
            prob_dict[language_name] = [self._calculate_sentence_probability(i, encoded_text)
                                        for i in self.n_gram_storages[language_name].values()]
            prob_dict[language_name] = sum(prob_dict[language_name]) / len(prob_dict[language_name])

        return prob_dict
