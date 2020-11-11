"""
Language detection using n-grams
"""
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
    checks = [
        isinstance(text, str),
        text != "",
    ]

    if not all(checks) or not any(letter.isalpha() for letter in text):
        return ()

    # generate indexes to split
    split_indexes = []
    for index in range(len(text[:-2])):
        conditions = [not text[index].isalpha(),
                      not text[index].isdigit(),
                      text[index + 1] == " ",
                      text[index + 2].isupper()]
        if all(conditions):
            split_indexes.append(index)

    # split text
    prev_split_point = 0
    split_text = []
    for index_split in split_indexes + [-1]:
        sentence = "".join([word for word in text[prev_split_point:index_split].lower()
                            if word.isalpha() or word == " "])
        split_text.append(tuple([tuple(f"_{word}_") for word
                                 in sentence.split()]))
        prev_split_point = index_split + 2
    return tuple(split_text)


# 4
class LetterStorage:

    def __init__(self, sentence=""):
        self.storage = {}

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """

        index_letter = 0
        checks = [
            isinstance(letter, str),
            letter != "",
        ]

        if not all(checks):
            return 1
        if letter not in self.storage.keys():
            self.storage[letter] = index_letter + 1
            index_letter += 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter in self.storage.keys():
            return self.storage[letter]
        return -1

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """

        if not isinstance(corpus, tuple):
            return 1

        corpus_managed = tuple(set([let for word in corpus for let in word]))

        for letter in corpus_managed:
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
    if not isinstance (corpus, tuple) or type(storage) in [int, str, list, tuple, dict, float, bool] or \
            storage is None:
        return ()

    storage.update(corpus)

    encoded = tuple([tuple(tuple(storage.get_id_by_letter(letter) for letter in word) for word in corpus[sent_in])
                     for sent_in in range(len(corpus))])

    return encoded


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

        # i will make it in generator, but later ;)
        n_grams = []
        for sent_in in range(len(encoded_text)):  # предложение
            sent = []
            for word in encoded_text[sent_in]:  # слово в предложении
                encoded_word = []
                for i in range(len(word) - self.size + 1):
                    encoded_word.append(tuple(word[i:i + self.size]))
                sent.append(tuple((encoded_word)))
            n_grams.append(tuple(sent))
        self.n_grams = tuple(n_grams)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_grams:
            return 1
        average = [n_gram for sent in self.n_grams for word in sent for n_gram in word]

        self.n_gram_frequencies = {n_gram: average.count(n_gram) for n_gram in average}
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1
        # please, check if i got it right, i think not
        for n_gram in self.n_gram_frequencies.keys():
            sum_n_grams = [self.n_gram_frequencies[l_gram] for l_gram in self.n_gram_frequencies.keys()
                           if l_gram[0] == n_gram[0]]
            self.n_gram_log_probabilities[n_gram] = log(self.n_gram_frequencies[n_gram] / sum(sum_n_grams))
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """


# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2,), top_k: int = 10):
        pass

    def new_language(self, encoded_text: tuple, language_name: str) -> int:
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """
        pass

    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        pass

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
