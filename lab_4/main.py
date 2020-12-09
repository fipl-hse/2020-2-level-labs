"""
Lab 4
"""
from random import randint
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    if text == '':
        return ()
    text = text.lower()
    text = text.replace('\n', ' ')
    text = text.replace('!', '.')
    text = text.replace('?', '.')
    while '  ' in text:
        text = text.replace('  ', ' ')
    ready = ''
    sentences = []
    final = []
    if '.' not in text:
        return ()
    for symbol in text:
        if symbol.isalpha() or symbol == ' ' or symbol == '.':
            ready += symbol
    ready = ready.split('.')
    for element in ready:
        sentences.append(element)
    for one in sentences:
        if len(one) != 0:
            new_line = []
            one = one.split()
            for word in one:
                if len(word) != 0:
                    new_line.append(word)
            new_line.append('<END>')
            final.extend(new_line)
    return tuple(final)
    pass


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if word not in self.storage and isinstance(word, str) and word != '':
            self.storage[word] = len(self.storage.keys())
            return self.storage[word]
        elif word in self.storage:
            return self.storage[word]
        else:
            raise ValueError

    def get_id(self, word: str) -> int:
        if not isinstance(word, str):
            raise ValueError
        if word in self.storage:
            return self.storage.get(word)
        else:
            raise KeyError

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int):
            raise ValueError
        if word_id not in self.storage.values():
            raise KeyError
        word_id = list(self.storage.values()).index(word_id)
        return list(self.storage.keys())[word_id]

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple) or corpus is None:
            raise ValueError
        for word in corpus:
            x = self._put_word(word)
            if x is None:
                self._put_word(word)
        return corpus


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    code_text = []
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError
    for el in storage.storage.keys():
        if not isinstance(el, str):
            raise ValueError
    for el in text:
        if not isinstance(el, str):
            raise ValueError
    for word in text:
        word = storage.get_id(word)
        code_text.append(word)
    return tuple(code_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie
        pass

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple):
            raise ValueError
        if len(context) != self._n_gram_trie.size - 1:
            raise ValueError
        max = 0
        new_part = None
        for el in self._n_gram_trie.n_gram_frequencies.keys():
            if el[:-1] == context:
                if self._n_gram_trie.n_gram_frequencies[el] > max:
                    max = self._n_gram_trie.n_gram_frequencies[el]
                    new_part = el[-1]
        if new_part is None:
            for el in self._n_gram_trie.uni_grams.keys():
                if self._n_gram_trie.uni_grams[el] > max:
                    max = self._n_gram_trie.uni_grams[el]
                    new_part = el[0]
        return new_part

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or context is None:
            raise ValueError
        if not context:
            raise ValueError
        end_token = self._word_storage.get_id('<END>')
        sentence = list(context)
        size = len(context)
        for _ in range(20):
            sentence.append(self._generate_next_word(tuple(sentence[-size:])))
            if sentence[-1] == end_token:
                break
        else:
            sentence.append(end_token)
        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        text = []
        size = self._n_gram_trie.size
        for i in range(number_of_sentences):
            text.extend(self._generate_sentence(context))
            context = tuple(text[-size:-1])
        return tuple(text)


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
