"""
Language detection using n-grams
"""
import re
import math
import copy

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
    if not any(letter in text for letter in 'abcdefghijklmnopqrstuvwxyz'):
        return ()
    result = []
    current_sent = []
    new_text = ''
    for sign in text:
        if sign != sign.lower():
            new_text += 2*sign  # That is done for the further split by dot, space and capital letter.
        elif sign in 'abcdefghijklmnopqrstuvwxyz!?,. ':
            new_text += sign.lower()
    new_text = new_text[1:]
    new_text = re.split(r'[.]\ [A-Z]', new_text)
    for sent in new_text:
        sent = re.sub(r'[!?.,]', '', sent)
        sent = sent.split()
        for word in sent:
            word = word.lower()
            current_word = tuple('_' + ''.join(word) + '_')
            current_sent.append(current_word)
        current_sent = tuple(current_sent)
        result.append(current_sent)
        current_sent = []
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
        letters = 'abcdefghijklmnopqrstuvwxyz_'
        if not isinstance(letter, str) or letter not in 'abcdefghijklmnopqrstuvwxyz_':
            return 1
        if letter not in self.storage.keys():
            self.storage[letter] = letters.index(letter)
        return 0


    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) or letter not in 'abcdefghijklmnopqrstuvwxyz_' \
                or letter not in self.storage.keys():
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
                for sign in word:
                    self._put_letter(sign)
        return 0




# 6
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    if not isinstance (corpus, tuple) or not isinstance(storage, LetterStorage):
        return ()
    result = []
    current_sent = []
    current_word = []
    for sentence in corpus:
        for word in sentence:
            for sign in word:
                storage._put_letter(sign)
                current_word.append(storage.get_id_by_letter(sign))
            current_sent.append(tuple(current_word))
            current_word = []
        result.append(tuple(current_sent))
        current_sent = []
    result = tuple(result)
    return result


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
        if not isinstance (encoded_text, tuple):
            return 1
        result = []
        current_word = []
        for sentence in encoded_text:
            current_sent = []
            for word in sentence:
                counter = 0
                for number in range(0, len(word) - self.size + 1):
                    current_word.append(tuple(word[counter:self.size + counter]))
                    counter += 1
                current_sent.append(tuple(current_word))
                current_word = []
            result.append(tuple(current_sent))
        self.n_grams = tuple(result)
        return 0


    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        for sentence in self.n_grams:
            for word in sentence:
                for gram in set(word):
                    if gram not in self.n_gram_frequencies.keys():
                        self.n_gram_frequencies[gram] = 0
                    self.n_gram_frequencies[gram] += word.count(gram)
        if len(self.n_gram_frequencies) == 0:
            return 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        for gram in self.n_gram_frequencies.keys():
            current_summ = 0
            for key in self.n_gram_frequencies.keys():
                if isinstance(key, int):
                    print(key, self.n_gram_frequencies[key])
                if key[0:-1] == gram[0:-1]:
                    current_summ += self.n_gram_frequencies[key]
            self.n_gram_log_probabilities[gram] = math.log(self.n_gram_frequencies[gram]/current_summ)
        if len(self.n_gram_log_probabilities) == 0:
            return 1
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance (k, int) or k <= 0:
            return ()
        freq_list = list(self.n_gram_frequencies.items())
        freq_list.sort(key=lambda x: x[1], reverse=True)
        ranged_grams = []
        for gram in freq_list:
            ranged_grams.append(gram[0])
        return tuple(ranged_grams[0:k])




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
        if not isinstance (encoded_text, tuple) or not isinstance(language_name, str):
            return 1
        for element in encoded_text:
            if not isinstance(element, tuple):
                return 1
        self.n_gram_storages[language_name] = {}
        for number in self.trie_levels:
            language_data = NGramTrie(number)
            language_data.fill_n_grams(encoded_text)
            language_data.calculate_n_grams_frequencies()
            language_data.calculate_log_probabilities()
            self.n_gram_storages[language_name][number] = language_data
        return 0

    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        if not isinstance(first_n_grams, tuple) or not isinstance (second_n_grams, tuple):
            return -1
        for element1, element2 in zip(first_n_grams, second_n_grams):
            if not isinstance(element1, tuple) or not isinstance(element2, tuple):
                return -1
        result = 0
        for gram in first_n_grams:
            if gram in second_n_grams:
                result += abs(first_n_grams.index(gram) - second_n_grams.index(gram))
            else:
                result += len(second_n_grams)
        return result

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple) or len(encoded_text) == 0:
            return {}
        for element in encoded_text:
            if not isinstance(element, tuple):
                return {}
        LanguageDetector.new_language(self, encoded_text, 'Unknown language')
        result_dict = {}
        for language, information in self.n_gram_storages.items():
            summ = 0
            counter = 0
            for value1, value2 in zip(information.values(), self.n_gram_storages['Unknown language'].values()):
                summ += self._calculate_distance(value1.top_n_grams(self.top_k), value2.top_n_grams(self.top_k))
                counter += 1
            result_dict[language] = summ/counter
        del result_dict['Unknown language']
        return result_dict


# 10
class ProbabilityLanguageDetector(LanguageDetector):

    def _calculate_sentence_probability(self, n_gram_storage: NGramTrie, sentence_n_grams: tuple) -> float:
        """
        Calculates sentence probability
        :param n_gram_storage: a filled NGramTrie with log-probabilities
        :param sentence_n_grams: n-grams from a sentence
        :return: a probability of a sentence
        """
        if not isinstance(n_gram_storage, NGramTrie) or not isinstance(sentence_n_grams, tuple):
            return -1
        n_gram_storage.n_grams = sentence_n_grams
        result = 0
        for value in n_gram_storage.n_gram_log_probabilities.values():
            result += value
        return result

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        if not isinstance(encoded_text, tuple):
            return {}
        result_dict = {}
        detect_dict = LanguageDetector.detect_language(self, encoded_text)
        for key, value in detect_dict.items():
            value = 0
            for number in self.trie_levels:
                object = NGramTrie(number)
                n_grams = object.fill_n_grams(encoded_text)
                value += self._calculate_sentence_probability(object, n_grams)
            result_dict[key] = value
        return result_dict

