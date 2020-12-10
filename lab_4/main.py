"""
Lab 4
"""
import re
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    sentences = re.split('[!?.] |[!?.]\n', text)
    list_tokens = []
    for sentence in sentences:
        tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if tokens:
            list_tokens.extend(tokens + ['<END>'])

    return tuple(list_tokens)


class WordStorage:  
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or word == '':
            raise ValueError

        if word not in self.storage:
            self.storage[word] = len(self.storage) + 1
        return self.storage.get(word)

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or word == '':
            raise ValueError

        if word not in self.storage:
            raise KeyError
        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int):
            raise ValueError

        for word in self.storage:
            if self.storage[word] == word_id:
                return word
        raise KeyError


    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError
        for word in corpus:
            self._put_word(word)


    def encode_text(storage: WordStorage, text: tuple) -> tuple:
        if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
            raise ValueError
        return tuple(storage.get_id(word) for word in text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        pass

    def _generate_next_word(self, context: tuple) -> int:
        pass

    def _generate_sentence(self, context: tuple) -> tuple:
        pass

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        pass

    def public_method(self):
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
