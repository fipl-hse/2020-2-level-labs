"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    tokens = []
    sentences = re.split('[.!?]', text)
    for sent in sentences:
        tok_sent = re.sub('[^a-z \n]', '', sent.lower()).split()
        if tok_sent:
            tokens.extend(tok_sent + ['<END>'])
    return tuple(tokens)


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
        for word, w_id in self.storage.items():
            if word_id == w_id:
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
    encoded_text = []
    for word in text:
        encoded_text.append(storage.get_id(word))
    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError
        freq_cont = {}
        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if context == n_gram[:self._n_gram_trie.size - 1]:
                freq_cont[n_gram] = freq
        if not freq_cont:
            top_n_gram = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=False)
            return top_n_gram[-1][-1]
        top_context_n_gram = sorted(freq_cont, key=freq_cont.get, reverse=False)
        return top_context_n_gram[-1][-1]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError
        list_cont = list(context)
        for i in range(20):
            word = self._generate_next_word(context)
            list_cont.append(word)
            if list_cont[-1] != self._word_storage.storage['<END>']:
                list_cont.append(self._word_storage.storage['<END>'])
            else:
                break
        return tuple(list_cont)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError
        text = []
        for i in range(number_of_sentences):
            sent = self._generate_sentence(context)
            if sent[len(context) - 1] == self._word_storage.storage['<END>']:
                sent = sent[len(context):]
            text.extend(sent)
            context = tuple(text[-len(context):])
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
