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

    sentences = re.split(r'\W{1,3}\s(?=[A-Z])', text)
    result = []

    for sentence in sentences:
        sent = []
        for token in re.sub('[^a-z ]', '', sentence.lower()).split():
            word = []
            for index, letter in enumerate(token):
                if index == 0:
                    word += '_' + letter
                elif index == len(token) - 1:
                    word += letter + '_'
                    sent.append(tuple(word))
                else:
                    word += letter
        if sent:
            result.append(tuple(sent))

    return tuple(result)


# 4
class LetterStorage:

    def __init__(self):
        LetterStorage.storage = {}

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str):
            return 1

        if letter not in self.storage:
            letter_id = 0
            self.storage[letter] = letter_id
            letter_id += 1

        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) or not letter in self.storage:
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
    if not isinstance(storage, LetterStorage) or not isinstance(corpus,tuple):
        return ()

    encode_corp = []
    encode_sentence = []
    for word in corpus:
        encode_word = list(word)
        for index, letter in enumerate(word):
            encode_word.pop(index)
            encode_word.insert(index, storage.get_id_by_letter(letter))
        encode_sentence.append(tuple(encode_word))
    if encode_sentence:
        encode_corp.append(tuple(encode_sentence))

    return tuple(encode_corp)


# 6
class NGramTrie:

    def __init__(self, n: int):
        NGramTrie.size = n
        NGramTrie.n_grams = ()
        NGramTrie.n_gram_frequencies = {}
        NGramTrie.n_gram_log_probabilities = {}

    def fill_n_grams(self, encoded_text: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(encoded_text, tuple):
            return 1

        new_text = []
        for sentence in encoded_text:
            sent = []
            for word in sentence:
                new_word = []
                for index, character in enumerate(word):
                    n_gram = []
                    number = self.size
                    if index != len(word) - 1:
                        while self.size - number < 1:
                            n_gram.append(character)
                            n_gram.append(word[index + 1])
                            number -= 1
                        new_word.append(tuple(n_gram))
                sent.append(tuple(new_word))
            new_text.append(tuple(sent))
            self.n_grams = tuple(new_text)

        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_grams:
            return 1

        all_n_grams = ()
        for sentence in self.n_grams:
            for word in sentence:
                all_n_grams += word
        set_n_grams = set(list(all_n_grams))
        self.n_gram_frequencies = {n_gram: list(all_n_grams).count(n_gram) for n_gram in set_n_grams}

        return 0

    def calculate_log_probabilities(self) -> int:  # не все так сладко (почему в тестах 12, а не 17?)
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1
        occurrence_number = 0
        for character in self.n_gram_frequencies.values():
            occurrence_number += character
        self.n_gram_log_probabilities = {n_gram: math.log(self.n_gram_frequencies[n_gram] / occurrence_number)
                                         for n_gram in self.n_gram_frequencies.keys()}

        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int):
            return ()
        list_output = sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)
        return tuple(list_output[:k])


# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2,), top_k: int = 10):
        LanguageDetector.trie_levels = trie_levels
        LanguageDetector.top_k = top_k
        LanguageDetector.n_gram_storages = {}

    def new_language(self, encoded_text: tuple, language_name: str) -> int:
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(encoded_text, tuple) or not isinstance(language_name, str):
            return 1
        for character in encoded_text:
            if not isinstance(character, tuple):
                return 1

        self.n_gram_storages[language_name] = {n: NGramTrie(n) for n in self.trie_levels}
        return 0

    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        if not isinstance(first_n_grams, tuple) or not isinstance(second_n_grams, tuple):
            return -1
        for character_1, character_2 in zip(first_n_grams, second_n_grams):
            if not isinstance(character_1, tuple) or not isinstance(character_2, tuple):
                return -1

        distance = 0
        for index, n_gram in enumerate(first_n_grams):
            if n_gram in second_n_grams:
                distance += math.fabs(index - second_n_grams.index(n_gram))

        return distance

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple):
            return {}
        for character in encoded_text:
            if not isinstance(character, tuple):
                return {}
        print(self.n_gram_storages)
        top_eng = self.n_gram_storages['english'][3]
        print('see:', top_eng)

        for language in self.n_gram_storages.keys():

            a = NGramTrie(3)  # self.n_gram_storages[language].values()
            print(a)
            NGramTrie.fill_n_grams(a, self.n_gram_storages[language])
            print(self.top_k, NGramTrie.top_n_grams(a, self.top_k))
            print({language: self._calculate_distance(encoded_text, NGramTrie.top_n_grams(a, self.top_k))
                    for language in self.n_gram_storages.keys()})

        return {language: self._calculate_distance(encoded_text, self.n_gram_storages[language])
                for language in self.n_gram_storages.keys()}


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







