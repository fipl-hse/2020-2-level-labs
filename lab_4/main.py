"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re

def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    sentences_list = re.split('[.!?]|\n', text)
    tokens_list = []
    for sentence in sentences_list:
        separ = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if not separ:
            continue
        separ.append('<END>')
        for word in separ:
            tokens_list.append(word)
    return tuple(tokens_list)


class WordStorage:
    def __init__(self):
        self.storage = {}
        self.value = 1

    def _put_word(self, word: str):
        if not isinstance(word, str) or len(word) == 0:
            raise ValueError
        if word not in self.storage:
            self.storage[word] = self.value
            self.value += 1
            return 1
        if word in self.storage:
            return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or not word:
            raise ValueError
        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int) or not word_id:
            raise ValueError
        for key, value in self.storage.items():
            if word_id == value:
                return key
            else:
                raise KeyError

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError
        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError
    encode_text = []
    for word in text:
        encode_text.append(storage.get_id(word))
    return tuple(encode_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        pass

    def _generate_next_word(self, context: tuple) -> int:
        pass

    def _generate_sentence(self, context: tuple) -> tuple:
        pass

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        pass


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
