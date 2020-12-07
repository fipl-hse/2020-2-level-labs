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
            if w_id == word_id:
                return word
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
    return tuple(storage.get_id(word) for word in text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        same_begin = [n_gram for n_gram in self._n_gram_trie.n_grams if context == n_gram[:len(context)]]
        if same_begin:
            top_n_grams = sorted(same_begin, key=self._n_gram_trie.n_gram_frequencies.get, reverse=True)
            return top_n_grams[0][-1]
        top_ini_grams = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
        return top_ini_grams[0][0]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        generated_sent = list(context)
        for _ in range(20):
            generated_sent.append(self._generate_next_word(tuple(generated_sent[-(len(context)):])))
            if generated_sent[-1] == self._word_storage.storage['<END>']:
                break
        else:
            generated_sent.append(self._word_storage.storage['<END>'])
        return tuple(generated_sent)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        generated_text = []
        for _ in range(number_of_sentences):
            new_sent = self._generate_sentence(context)
            if new_sent[len(context) - 1] == self._word_storage.get_id('<END>'):
                new_sent = new_sent[len(context):]
            generated_text.extend(list(new_sent))
            context = new_sent[-len(context):]
        return tuple(generated_text)

    def public_method(self):
        pass


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if not isinstance(word, int) or not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError
        context_freq = 0.0

        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if n_gram[:len(context)] == context:
                context_freq += freq

        return self._n_gram_trie.n_gram_frequencies.get(context + (word,), 0) / context_freq if context_freq \
            else context_freq

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError
        for word_id in context:
            if word_id > len(self._word_storage.storage):
                raise ValueError

        max_lh_dict = {}
        for word_id in self._word_storage.storage.values():
            max_lh_dict[word_id] = self._calculate_maximum_likelihood(word_id, context)
        if max_lh_dict:
            return sorted(max_lh_dict, key=max_lh_dict.get, reverse=True)[0]
        return sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)[0][0]

    def public_method_2(self):
        pass


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass

    def public_method_3(self):
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple):
        raise ValueError

    text = []
    sentence = []
    for word_id in encoded_text:
        if word_id != storage.get_id('<END>'):
            if not sentence:
                real_word = storage.get_word(word_id)
                sentence.append(real_word[0].upper() + real_word[1:])
            else:
                sentence.append(storage.get_word(word_id))
        else:
            text.append(' '.join(sentence))
            sentence = []

    return tuple(text)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass
