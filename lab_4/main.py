"""
Lab 4
"""

import re
from lab_4.ngrams.ngram_trie import NGramTrie

def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    text = re.sub(r'[^a-z \.\?\!]', '', text.lower())
    text = re.sub(r'[\.\?\!]', ' <END> ', text)
    text = re.sub(' +', ' ', text).split(' ')
    prepared_text = [word for word in text if word]
    if prepared_text and prepared_text[-1] != '<END>':
        prepared_text.append('<END>')
    return tuple(prepared_text)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str):
            raise ValueError
        if word not in self.storage:
            self.storage[word] = len(self.storage)

        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or not word:
            raise ValueError
        if word not in self.storage:
            raise KeyError

        word_id = self.storage[word]
        return word_id

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int) or isinstance(word_id, bool):
            raise ValueError

        for word, id_num in self.storage.items():
            if id_num == word_id:
                return word
        raise KeyError

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError

        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(text, tuple) or not isinstance(storage, WordStorage):
        raise ValueError

    encoded_text = [storage.get_id(word) for word in text]
    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if (not isinstance(context, tuple) or
                not context or
                    len(context) != self._n_gram_trie.size - 1):
            raise ValueError

        n_gram_freq = {}
        for n_gram in self._n_gram_trie.n_grams:
            if n_gram[:len(context)] == context:
                n_gram_freq[n_gram] = self._n_gram_trie.n_gram_frequencies[n_gram]
        if n_gram_freq:
            top_freq = sorted(n_gram_freq, key=n_gram_freq.get, reverse=True)[0]
            return top_freq[-1]
        top_freq = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)[0]
        return top_freq[0]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or not context:
            raise ValueError

        end_id = self._word_storage.get_id('<END>')
        generated_sentence = [word_id for word_id in context[:self._n_gram_trie.size - 1] if end_id not in context]
        for _ in range(20):
            new_word = self._generate_next_word(context)
            generated_sentence.append(new_word)
            context = context[:self._n_gram_trie.size - 1] + (new_word,)
            context = context[-(self._n_gram_trie.size - 1):]
            if end_id in generated_sentence:
                return tuple(generated_sentence)
        generated_sentence.append(self._word_storage.get_id('<END>'))
        return tuple(generated_sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if (not isinstance(context, tuple) or not context or
                not isinstance(number_of_sentences, int) or
                    isinstance(number_of_sentences, bool)):
            raise ValueError

        generated_text = []
        for _ in range(number_of_sentences):
            generated_sentence = self._generate_sentence(context)
            context = generated_sentence[-len(context):]
            generated_text.extend(list(generated_sentence))
        return tuple(generated_text)

    def some_function_for_lint_1(self):
        pass


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if (not isinstance(word, int) or
                isinstance(word, bool) or
                    not isinstance(context, tuple) or
                        len(context) != self._n_gram_trie.size - 1):
            raise ValueError

        context_freq = len([n_gram for n_gram in self._n_gram_trie.n_grams if n_gram[:len(context)] == context])
        if not context_freq or context + (word,) not in self._n_gram_trie.n_gram_frequencies:
            return 0.0
        n_gram_freq = self._n_gram_trie.n_gram_frequencies[context + (word,)]
        return n_gram_freq / context_freq

    def _generate_next_word(self, context: tuple) -> int:
        if (not isinstance(context, tuple) or
                not context):
            raise ValueError

        for word_id in context:
            if word_id not in self._word_storage.storage.values():
                raise ValueError

        likelihood = {}
        for word_id in self._word_storage.storage.values():
            likelihood[word_id] = self._calculate_maximum_likelihood(word_id, context)
        if likelihood:
            top_freq = sorted(likelihood, key=likelihood.get, reverse=True)[0]
            return top_freq
        top_freq = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)[0]
        return top_freq[0]


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple):
        raise ValueError

    text = [storage.get_word(word_id) for word_id in encoded_text]
    sentence = []
    decoded_text = []
    for idx, word in enumerate(text):
        if idx == 0 or text[idx - 1] == '<END>':
            word = word[0].upper() + word[1:]
        if word != '<END>':
            sentence.append(word)
        else:
            decoded_text.append(' '.join(sentence))
            sentence = []
    return tuple(decoded_text)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass
