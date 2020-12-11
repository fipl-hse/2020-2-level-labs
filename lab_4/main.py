"""
Lab 4
"""

import re
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    sentences = re.split('[.!?]', text)
    list_words = []
    for sentence in sentences:
        tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if not tokens:
            continue
        list_words += tokens + ['<END>']

    return tuple(list_words)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or word == None:
            raise ValueError
        if word not in self.storage:
            self.storage[word] = len(self.storage) + 1


    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or word == None:
            raise ValueError
        if word not in self.storage:
            raise KeyError
        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, str) or word_id == None:
            raise ValueError
        if word_id not in self.storage.values():
            raise KeyError
        for word, id_word in self.storage.items():
            if word_id == id_word:
                return word

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple) or (corpus and not isinstance(corpus[0], str)):
            raise ValueError
        for token in corpus:
            self._put_word(token)



def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError
    return tuple(storage.get_id(word) for word in text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self.word_storage = word_storage
        self.n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError
        gaining_context = self.get_most_frequent_gram(context)
        if not gaining_context:
            return max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]
        return gaining_context[-1]
    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError
        sentence = list(context)
        for num in range(20):
            sentence.append(self._generate_next_word(tuple(sentence[-(len(context)):])))
            if sentence[-1] == self._word_storage.storage['<END>']:
                break
        else:
            sentence.append(self._word_storage.storage['<END>'])
        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        text = self._generate_sentence(context)  # with first sentence

        for num in range(2, number_of_sentences + 1):
            sentence = self._generate_sentence(text[-self.context_size:])[self.context_size + 1:]
            text += sentence
        return text


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
