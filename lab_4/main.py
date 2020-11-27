"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re

def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    elif not text:
        return ()

    sentences_in_text = re.split('[\n.?!]', text)
    new_text = []

    for sentence in sentences_in_text:
        if len(sentence.strip()):
            new_sentences = re.sub('[^a-z \n]', '', sentence.lower()).split()
            if len(new_sentences):
                new_text.append(new_sentences + ['<END>'])

    full_text = []
    for new_sentence in new_text:
        for word in new_sentence:
            full_text.append(word)

    return tuple(full_text)


class WordStorage:
    def __init__(self):
        self.storage = {}
        self.id = 1

    def _put_word(self, word: str):

        if not isinstance(word, str) \
                or not len(word):
            raise ValueError

        if word not in self.storage:
            self.storage[word] = self.id
            self.id += 1

        return self.storage[word]

    def get_id(self, word: str) -> int:

        if not isinstance(word, str):
            raise ValueError

        for word1 in self.storage:
            if word1 in self.storage:
                if word1 == word:
                    return self.storage[word]
        raise KeyError

    def get_word(self, word_id: int) -> str:

        if not isinstance(word_id, int):
            raise ValueError

        for word, word_id1 in self.storage.items():
            if word_id1 == word_id:
                return word

        raise KeyError

    def update(self, corpus: tuple):

        if not isinstance(corpus, tuple):
            raise ValueError

        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:

    if not isinstance(storage, WordStorage)\
            or not isinstance(text, tuple):
        raise ValueError

    encoded_text = []

    for word in text:
        encoded_text.append(storage.get_id(word))

    return tuple(encoded_text)


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
