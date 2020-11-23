import re
from math import log

"""
Language detection using n-grams
"""


def universal_input_checker(*args_checker):
    def dec_func(f):
        def wrapper(*args, **kwargs):
            types = args_checker[1:]
            for i, el in enumerate(types):
                if not isinstance(args[i], el):
                    return args_checker[0]
            for x in args:
                if x is None:
                    return args_checker[0]
            return f(*args, **kwargs)

        return wrapper

    return dec_func


def universal_input_checker_method(*args_checker):
    def dec_func(f):
        def wrapper(self, *args, **kwargs):
            types = args_checker[1:]
            for i, el in enumerate(types):
                if not isinstance(args[i], el):
                    return args_checker[0]
            for x in args:
                if x is None:
                    return args_checker[0]
            return f(self, *args, **kwargs)

        return wrapper

    return dec_func


# 4
def my_replace(word: list, letter_old: str, letter_new: str) -> list:
    result = []
    for letter in word:
        if letter == letter_old:
            result.append(letter_new)
        else:
            result.append(letter)
    return result


@universal_input_checker((), str)
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
    result = []
    extra = set("""1234567890-=@#$%^&*()_+,/<>;:'"[{}]"'""")
    for letter in extra:
        text = text.replace(letter, "")

    # text = text.lower().split(r"[.?!]")
    text = re.split(r"[.?!]", text.lower())
    for sentence in text:
        sentence_words = []
        sentence = sentence.split()
        for word in sentence:
            word_letters = list("_" + word + "_")
            word_letters = my_replace(word_letters, "ö", "oe")
            word_letters = my_replace(word_letters, "ü", "ue")
            word_letters = my_replace(word_letters, "ä", "ae")
            word_letters = my_replace(word_letters, "ß", "ss")
            sentence_words.append(tuple(word_letters))
        if () != tuple(sentence_words):
            result.append(tuple(sentence_words))
    return tuple(result)


# 4
class LetterStorage:

    def __init__(self):
        self.count = 0
        self.storage = {}

    @universal_input_checker_method(1, str)
    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if letter in self.storage:
            return 0
        else:
            self.storage[letter] = self.count
            self.count += 1
            return 0

    @universal_input_checker_method(-1, str)
    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter in self.storage:
            return self.storage[letter]
        else:
            return -1

    @universal_input_checker_method(1, tuple)
    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        for sentence in corpus:
            for word in sentence:
                for letter in word:
                    self._put_letter(letter)
        return 0

a = LetterStorage()
corpus = tokenize_by_sentence("I am gay")
a.update(corpus)

@universal_input_checker((), LetterStorage, tuple)
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    result = []
    for sentence in corpus:
        result_sentence = []
        for word in sentence:
            result_word = []
            for letter in word:
                id = storage.get_id_by_letter(letter)
                result_word.append(id)
            result_sentence.append(tuple(result_word))
        result.append(tuple(result_sentence))
    return tuple(result)
#?как должен выглядеть вызов этой функции?
#print(encode_corpus(a, corpus))
# 6
class NGramTrie:

    def __init__(self, n: int):
        self.size = n
        self.n_grams = ()
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

    @universal_input_checker_method(1, tuple)
    def fill_n_grams(self, encoded_text: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        """
        result = []
        for sentence in encoded_text:
            sentence_res = []
            for word in sentence:
                word_res = []
                for i in range(len(word) - self.size + 1):
                    word_res.append(tuple(word[i:i + self.size]))
                sentence_res.append(tuple(word_res))
            result.append(tuple(sentence_res))
        self.n_grams = tuple(result)
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
                    if self.n_gram_frequencies.get(n_gram):
                        self.n_gram_frequencies[n_gram] += 1
                    else:
                        self.n_gram_frequencies[n_gram] = 1
        return 0

    def calculate_log_probabilities(self) -> int: #?
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if len(self.n_gram_frequencies) == 0:
            return 1

        for n_gram, freq in self.n_gram_frequencies.items():
            all_events = 0
            for n_gram2, freq2 in self.n_gram_frequencies.items():
                if n_gram2[0: self.size - 1] == n_gram[0: self.size - 1]:
                    all_events += freq2
            self.n_gram_log_probabilities[n_gram] = log(freq / all_events)

        return 0

    @universal_input_checker_method((), int)
    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        n_grams_list = [(n_gram, freq) for n_gram, freq in self.n_gram_frequencies.items()]
        n_grams_list = sorted(n_grams_list, key=lambda x: -x[1])
        return tuple([x[0] for x in n_grams_list[0: k]])


# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2,), top_k: int = 10):
        self.top_k = top_k
        self.trie_levels = trie_levels
        self.n_gram_storages = {}

    @universal_input_checker_method(1, tuple, str)
    def new_language(self, encoded_text: tuple, language_name: str) -> int:
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """

        self.n_gram_storages[language_name] = {}

        for i in self.trie_levels:
            trie = NGramTrie(i)
            trie.fill_n_grams(encoded_text)
            trie.calculate_n_grams_frequencies()
            trie.calculate_log_probabilities()
            self.n_gram_storages[language_name][i] = trie

        return 0

    def is_number(self, x):
        if x is None:
            return False
        if str(type(x)) == "<class 'bool'>":
            return False
        if not isinstance(x, int):
            return False
        return True

    @universal_input_checker_method(-1, tuple, tuple)
    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        for n_gram in first_n_grams:
            if not isinstance(n_gram, tuple):
                return -1
            for element in n_gram:
                if not self.is_number(element):
                    return -1
        for n_gram in second_n_grams:
            if not isinstance(n_gram, tuple):
                return -1
            for element in n_gram:
                if not self.is_number(element):
                    return -1
        distance = 0
        for i, n_gram1 in enumerate(first_n_grams):
            index = -1
            for j, n_gram2 in enumerate(second_n_grams):
                if n_gram1 == n_gram2:
                    index = j
                    break
            if index == -1:
                distance += len(second_n_grams)
            else:
                distance += abs(index - i)
        return distance

    @universal_input_checker_method({}, tuple)
    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        dict_result = {}
        for lang, storage in self.n_gram_storages.items():
            dict_result[lang] = 1000000000
            for i in self.trie_levels:
                trie = NGramTrie(i)
                trie.fill_n_grams(encoded_text)
                dict_result[lang] += self._calculate_distance(self.n_gram_storages[lang][i].top_n_grams(self.top_k), trie.top_n_grams(self.top_k))
            dict_result[lang] /= len(self.trie_levels)
        return dict_result

language_detector = LanguageDetector((3, ), 10)

patches_ngrams = ((1, 2), (3, 4), (7, 8), (9, 10), (5, 6), (13, 14))

expected = -1
bad_inputs = [[], {}, '', 1, -1, 9.22, None, True, (None,)]
for bad_input in bad_inputs:
    actual_first = language_detector._calculate_distance(bad_input, patches_ngrams)
    actual_second = language_detector._calculate_distance(patches_ngrams, bad_input)
    print(actual_first, actual_second)


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
