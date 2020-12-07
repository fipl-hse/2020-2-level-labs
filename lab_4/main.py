"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re


def tokenize_by_sentence(text: str) -> tuple:
    wrong_circumstances = not isinstance(text, str) or isinstance(text, bool) \
                          or list(filter(lambda symbol: symbol.isalpha(), text)) == []  # строка из символов
    if wrong_circumstances:
        raise ValueError
    text = 'I have a cat.\nHis name is Bruno.'
    text = text.lower()
    text = re.split(r'[.?!][\n\s]', text)
    text_tuple = ''
    for sentence in text:
        for element in sentence:
            if element.isalpha() is False and element != ' ':
                sentence = sentence.replace(element, '')
        text_tuple += sentence + ' ' + '<END>' + ' '
    text_tuple = text_tuple[0:len(text_tuple) - 1]
    text_tuple = tuple(text_tuple.split(' '))
    return text_tuple


class WordStorage:
    def __init__(self):
        pass

    def _put_word(self, word: str):
        pass

    def get_id(self, word: str) -> int:
        pass

    def get_word(self, word_id: int) -> str:
        pass

    def update(self, corpus: tuple):
        pass


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    pass


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
