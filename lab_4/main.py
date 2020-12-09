"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re


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
        self.counter = 0

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
        elif word not in self.storage:
            raise KeyError

        return self.storage[word]

    def get_word(self, word_id: int) -> str:

        if not isinstance(word_id, int) or isinstance(word_id, bool):
            raise ValueError
        elif word_id not in list(self.storage.values()):
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
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def get_top_word(self):

        uni_gram_frequencies = list(self._n_gram_trie.uni_grams.items())
        uni_gram_frequencies.sort(key=lambda x: x[1], reverse=True)

        return uni_gram_frequencies[0][0][0]

    def _generate_next_word(self, context: tuple) -> int:

        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        n_gram_context = [n_gram for n_gram in self._n_gram_trie.n_gram_frequencies.keys()
                          if n_gram[:len(context)] == context]

        if not n_gram_context:
            return self.get_top_word()

        n_gram_context_freq = [self._n_gram_trie.n_gram_frequencies[n_gram] for n_gram in n_gram_context]
        n_gram_top = n_gram_context[n_gram_context_freq.index(max(n_gram_context_freq))]

        return n_gram_top[-1]

    def _generate_sentence(self, context: tuple) -> tuple:

        if not isinstance(context, tuple):
            raise ValueError

        generated_sentence = list(context)
        end_id = self._word_storage.get_id('<END>')
        for limit in range(20):
            generated_sentence.append(self._generate_next_word(tuple(generated_sentence[-len(context):])))
            if generated_sentence[-1] == end_id:
                return tuple(generated_sentence)

        generated_sentence.append(end_id)

        return tuple(generated_sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:

        if not isinstance(context, tuple):
            raise ValueError

        generated_text = self._generate_sentence(context)
        for number_sentence in range(number_of_sentences - 1):
            generated_text += self._generate_sentence(tuple(generated_text[-len(context):]))[len(context):]

        return generated_text


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:

        if (not isinstance(context, tuple) or not isinstance(word, int) or len(context) != self._n_gram_trie.size - 1
                or (word,) not in list(self._n_gram_trie.uni_grams.keys())):
            raise ValueError

        if context + (word,) not in self._n_gram_trie.n_grams:
            return 0.0

        n_gram_word_freq = self._n_gram_trie.n_gram_frequencies[context + (word,)]
        n_gram_context = len([n_gram for n_gram in self._n_gram_trie.n_gram_frequencies.keys()
                              if n_gram[:len(context)] == context])

        return n_gram_word_freq / n_gram_context

    def _generate_next_word(self, context: tuple) -> int:

        if (not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1 or
                not all([context_id <= len(self._word_storage.storage) for context_id in context])):
            raise ValueError

        likelihoods = {}
        for word_id in self._word_storage.storage_by_id.keys():
            likelihoods[word_id] = self._calculate_maximum_likelihood(word_id, context)

        likelihoods_sorted = list(likelihoods.items())
        likelihoods_sorted.sort(key=lambda x: x[1], reverse=True)

        return likelihoods_sorted[0][0] if likelihoods_sorted[0][0] else self.get_top_word()


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)
        self._n_gram_tries = (n_gram_trie,) + args
        self._n_gram_tries_by_size = {}
        self.fill_n_gram_tries()

    def fill_n_gram_tries(self):

        for n_gram_trie in self._n_gram_tries:
            if n_gram_trie.size not in self._n_gram_tries_by_size:
                self._n_gram_tries_by_size[n_gram_trie.size] = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:

        if (not isinstance(context, tuple) or not all([context_id <= len(self._word_storage.storage)
                                                       for context_id in context])):
            raise ValueError

        for generate_attempt in range(len(self._n_gram_tries)):

            n_gram_trie = self._n_gram_tries_by_size[len(context) + 1]

            if not isinstance(n_gram_trie, NGramTrie) or len(context) != n_gram_trie.size - 1:
                raise ValueError

            n_gram_context = [n_gram for n_gram in n_gram_trie.n_gram_frequencies.keys()
                              if n_gram[:len(context)] == context]

            if not n_gram_context:
                context = context[:-1]
                continue

            n_gram_context_freq = [n_gram_trie.n_gram_frequencies[n_gram] for n_gram in n_gram_context]
            n_gram_top = n_gram_context[n_gram_context_freq.index(max(n_gram_context_freq))]

            return n_gram_top[-1]


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:

    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple):
        raise ValueError

    decoded_text = []
    sentence = ''
    for word_id in encoded_text:
        if word_id == storage.get_id('<END>'):
            decoded_text.append(sentence)
            sentence = ''
            continue
        if not sentence:
            word = storage.get_word(word_id)[0].upper() + storage.get_word(word_id)[1:]
        else:
            word = ' ' + storage.get_word(word_id)
        sentence += word

    return tuple(decoded_text)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass
