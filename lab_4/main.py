"""
Lab 4
"""
import re
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    text = re.split(r'[.?!]\s', text)
    text_tokens = []
    for sentence in text:
        sentence = re.sub(r'[^\w\s]', '', sentence).lower().split()
        if sentence:
            sentence.append('<END>')
        text_tokens.extend(sentence)

    return tuple(text_tokens)


class WordStorage:
    def __init__(self):
        self.storage = {}
        self.storage_by_id = {}
        self.counter = 1

    def _put_word(self, word: str):
        if not isinstance(word, str) or not word:
            raise ValueError
        if word not in self.storage:
            self.storage[word] = self.counter
            self.storage_by_id[self.counter] = word
            self.counter += 1

        return self.get_id(word)

    def get_id(self, word: str) -> int:

        if not isinstance(word, str) or not word:
            raise ValueError
        if word not in self.storage:
            raise KeyError
        return self.storage[word]




    def get_word(self, word_id: int) -> str:

        if not isinstance(word_id, int) or isinstance(word_id, bool):
            raise ValueError
        if word_id not in list(self.storage.values()):
            raise KeyError
        self.storage_by_id = dict(storage_item[::-1] for storage_item in list(self.storage.items()))

        return self.storage_by_id[word_id]


    def update(self, corpus: tuple):

        if not isinstance(corpus, tuple):
            raise ValueError

        for token in corpus:
            self._put_word(token)



def encode_text(storage: WordStorage, text: tuple) -> tuple:

    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError

    storage.update(text)
    text_in_ids = [storage.get_id(token) for token in text]

    return tuple(text_in_ids)


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
