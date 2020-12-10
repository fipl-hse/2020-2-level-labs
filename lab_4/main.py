"""
Lab 4
"""

import re
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    sentences = re.split('[!?.] |[!?.]\n', text)
    token_list = []
    for sentence in sentences:
        tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if tokens:
            token_list.extend(tokens + ['<END>'])

    return tuple(token_list)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or not word:
            raise ValueError

        if word not in self.storage:
            self.storage[word] = len(self.storage) + 1
        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or not word:
            raise ValueError

        if word not in self.storage:
            raise KeyError
        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int) or not word_id:
            raise ValueError

        for word, id_w in self.storage.items():
            if id_w == word_id:
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
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        same_beginnig = [n_gram for n_gram in self._n_gram_trie.n_grams if context == n_gram[:len(context)]]
        if same_beginnig:
            top_n_grams = sorted(same_beginnig, key=self._n_gram_trie.n_gram_frequencies.get, reverse=True)
            return top_n_grams[0][-1]
        top_ini_grams = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
        return top_ini_grams[0][0]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        sent_generate = list(context)
        for _ in range(20):
            sent_generate.append(self._generate_next_word(tuple(sent_generate[-(len(context)):])))
            if sent_generate[-1] == self._word_storage.storage['<END>']:
                break
        else:
            sent_generate.append(self._word_storage.storage['<END>'])
        return tuple(sent_generate)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        text_generate = []
        for _ in range(number_of_sentences):
            new_sentance = self._generate_sentence(context)
            if new_sentance[len(context) - 1] == self._word_storage.get_id('<END>'):
                new_sentance = new_sentance[len(context):]
            text_generate.extend(list(new_sentance))
            context = new_sentance[-len(context):]
        return tuple(text_generate)


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
