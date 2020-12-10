"""
Lab 4
"""
import re
from functools import wraps

from ngrams.ngram_trie import NGramTrie


def universal_input_checker(*args_checker):
    def dec_func(func):
        @wraps(func)   # Переносит информацию (например docstring)
        def wrapper(*args, **kwargs):
            types = args_checker[1:]
            for i, element in enumerate(types):
                if not isinstance(args[i], element):
                    raise args_checker[0]  # f. e. ValueError
            for arg in args:
                if arg is None:
                    raise args_checker[0]
            return func(*args, **kwargs)

        return wrapper

    return dec_func


def universal_input_checker_method(*args_checker):
    def dec_func(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            types = args_checker[1:]
            for i, element in enumerate(types):
                if not isinstance(args[i], element):
                    raise args_checker[0]
            for arg in args:
                if arg is None:
                    raise args_checker[0]
            return func(self, *args, **kwargs)

        return wrapper

    return dec_func


@universal_input_checker(ValueError, str)
def tokenize_by_sentence(text: str) -> tuple:
    result = []
    extra = set("""1234567890-=@#$%^&*()_+,/<>;:'"[{}]"'""")
    for letter in extra:
        text = text.replace(letter, "")
    text = re.split(r"[.?!]", text.lower())
    for sentence in text:
        if sentence == '':
            continue
        sentence = sentence.split()
        for word in sentence:
            result.append(word)
        result.append('<END>')
    # if len(result) == 0:
    #    result.append('<END>')
    return tuple(result)


class WordStorage:

    def __init__(self):
        self.count = 0
        self.storage = {}

    @universal_input_checker_method(ValueError, str)
    def _put_word(self, word: str) -> int:
        if word not in self.storage:
            self.storage[word] = self.count
            self.count += 1
            return 0
        return 1

    @universal_input_checker_method(ValueError, str)
    def get_id(self, word: str) -> int:
        if word in self.storage:
            return self.storage[word]
        raise KeyError

    @universal_input_checker_method(ValueError, int)
    def get_word(self, word_id: int) -> str:
        for k, v in self.storage.items():
            if v == word_id:
                return k
        raise KeyError

    @universal_input_checker_method(ValueError, tuple)
    def update(self, corpus: tuple):
        for word in corpus:
            self._put_word(word)


@universal_input_checker(ValueError, WordStorage, tuple)
def encode_text(storage: WordStorage, text: tuple) -> tuple:
    result = []
    for word in text:
        my_id = storage.get_id(word)
        result.append(my_id)
    return tuple(result)


# corpus = tokenize_by_sentence("Im not GAY. I hope not")
# a = WordStorage()
# a.update(corpus)
# print(encode_text(a, corpus))


class NGramTextGenerator:

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self.storage = word_storage
        self._n_gram_trie = n_gram_trie
        self.trie = n_gram_trie

    @universal_input_checker_method(ValueError, tuple)
    def _generate_next_word(self, context: tuple) -> int:
        if len(context) < self.trie.size - 1:
            raise ValueError
        max_frequency = -1
        next_word_n_gram = ()
        top_word = ()
        top_freq = -1
        for uni_gram, freq in self.trie.uni_grams.items(): # the biggest frequency uni_gram
            if freq > top_freq:
                top_word = uni_gram
                top_freq = freq

        for n_gram in self.trie.n_grams:
            if context == tuple(n_gram[0:len(context)]):
                if self.trie.n_gram_frequencies[n_gram] > max_frequency:
                    next_word_n_gram = n_gram
                    max_frequency = self.trie.n_gram_frequencies[n_gram]
        if len(next_word_n_gram) == 0:
            return top_word[0]
        return next_word_n_gram[-1]

    @universal_input_checker_method(ValueError, tuple)
    def _generate_sentence(self, context: tuple) -> tuple:
        generated = 0
        last_word = -1
        result = []
        while generated < 20 and last_word != self.storage.get_id("<END>"):
            try:
                result.append(self._generate_next_word(context))
            except ValueError:
                result.append(self.storage.get_id("<END>"))
            generated += 1
            last_word = result[-1]
        if last_word != self.storage.get_id("<END>"):
            result.append(self.storage.get_id("<END>"))
        return tuple(result)

    @universal_input_checker_method(ValueError, tuple, int)
    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        result = []
        for i in range(number_of_sentences):
            temp = self._generate_sentence(context)
            for word in temp:
                result.append(word)
            context = temp[1:len(temp)]

        return tuple(result)


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        pass

    def _generate_next_word(self, context: tuple) -> int:
        pass


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    pass


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass
