"""
Lab 4
"""

## added test for empty inputs, incorrect num inputs
## added test for save and load model


import ast
from pprint import pprint
import re

from lab_4.ngrams.ngram_trie import NGramTrie
from lab_4 import validation


def tokenize_by_sentence(text: str) -> tuple:
    validation.ensure_type((text, str))
    validation.ensure_not_empty((text, ))

    clean_text = re.sub(r'[^.!?\w\s]', '', text)
    tokens = tuple(re.sub(r'([A-Z][\w\s]+)[.!?]?',
                          lambda x: x.group(1).lower() + ' <END>',
                          clean_text
                          ).split())
    return tokens


class WordStorage:

    def __init__(self):
        self.storage = {}
        self.reversed_storage = {}

    def _put_word(self, word: str) -> int:
        validation.ensure_type((word, str))
        validation.ensure_not_empty(word)

        if word not in self.storage:
            word_id = len(self.storage)
            self.storage[word] = word_id
            self.reversed_storage[word_id] = word

        return self.storage[word]

    def get_id(self, word: str) -> int:
        validation.ensure_type((word, str))
        validation.ensure_not_empty(word)

        return self.storage[word]

    def update_reversed_storage(self):
        self.reversed_storage = {value: key for key, value in self.storage.items()}

    def get_word(self, word_id: int) -> str:
        validation.ensure_type((word_id, int))
        validation.ensure_correct_int(word_id, null_is_available=True)

        if word_id not in self.reversed_storage:
            self.update_reversed_storage()

        return self.reversed_storage[word_id]

    def update(self, corpus: tuple):
        validation.ensure_type((corpus, tuple))

        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    validation.ensure_type(
        (storage, WordStorage),
        (text, tuple),
        )
    validation.ensure_not_empty(storage)

    return tuple(storage.get_id(word) for word in text)


class NGramTextGenerator:

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        validation.ensure_type((context, tuple))
        validation.ensure_length(context, self._n_gram_trie.size - 1)

        freqs = self._n_gram_trie.n_gram_frequencies
        max_freq = 0

        if any(n_gram for n_gram in freqs if n_gram[:-1] == context):
            for n_gram in freqs:
                if freqs[n_gram] > max_freq and n_gram[:-1] == context:
                    max_freq = freqs[n_gram]
                    max_n_gram = n_gram
        else:
            for uni_gram in self._n_gram_trie.uni_grams:
                if self._n_gram_trie.uni_grams[uni_gram] > max_freq:
                    max_freq = self._n_gram_trie.uni_grams[uni_gram]
                    max_n_gram = uni_gram
        return max_n_gram[-1]

    def _generate_sentence(self, context: tuple) -> tuple:
        validation.ensure_type((context, tuple))
        validation.ensure_not_empty(context)

        sent = context
        length = self._n_gram_trie.size - 1
        n_gram = sent[-length:]
        end_id = self._word_storage.get_id('<END>')
        for _ in range(20):
            sent += (self._generate_next_word(n_gram), )
            if sent[-1] == end_id:
                break
            n_gram = sent[-length:]
        else:
            sent += (end_id, )
        return sent

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        validation.ensure_type(
            (context, tuple),
            (number_of_sentences, int),
            )
        validation.ensure_not_empty(context)
        validation.ensure_correct_int(number_of_sentences)

        text = context
        length = self._n_gram_trie.size - 1
        for _ in range(number_of_sentences):
            text += self._generate_sentence(context)[length:]
            context = text[-length:]
        return text


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        validation.ensure_type(
            (word, int),
            (context, tuple),
            )
        validation.ensure_length(context, self._n_gram_trie.size - 1)
        validation.ensure_correct_int(word, null_is_available=True)

        current_n_gram = context + (word, )
        freq = self._n_gram_trie.n_gram_frequencies

        if current_freq := freq.get(current_n_gram, 0):
            common_freq = sum(
                freq[n_gram] for n_gram in freq
                if n_gram[:-1] == context
                )
            return current_freq / common_freq
        return 0

    def _generate_next_word(self, context: tuple) -> int:
        validation.ensure_type((context, tuple))
        validation.ensure_not_empty(context)
        validation.ensure_length(context, self._n_gram_trie.size - 1)

        self._word_storage.update_reversed_storage()

        likelihood = {}
        for word in self._word_storage.reversed_storage:
            if self._calculate_maximum_likelihood(word, context) in likelihood:
                likelihood[self._calculate_maximum_likelihood(word, context)].append(word)
            else:
                likelihood[self._calculate_maximum_likelihood(word, context)] = [word]

        max_likelihood = max(likelihood.keys())

        return likelihood[max_likelihood][0]


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    validation.ensure_type(
        (storage, WordStorage),
        (encoded_text, tuple),
        )
    validation.ensure_not_empty(storage, encoded_text)

    text = ' '.join((storage.get_word(word) for word in encoded_text)) + ' '
    text = text.split(' <END> ')
    text = tuple(sent.capitalize() for sent in text)[:-1]

    return text


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

        tries = [n_gram_trie] + list(args)
        self._n_gram_tries = sorted(tries, key=lambda trie: trie.size)[::-1]

    def _generate_next_word(self, context: tuple) -> int:
        validation.ensure_type((context, tuple))
        validation.ensure_not_empty(context)

        max_trie_size = len(context) + 1
        self._n_gram_tries = [trie for trie in self._n_gram_tries if trie.size <= max_trie_size]

        for trie in self._n_gram_tries:
            self._n_gram_trie = trie
            if n_gram := super()._generate_next_word(context):
                return n_gram
            context = context[:-1]
        return n_gram


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    validation.ensure_type(
        (model, NGramTextGenerator),
        (path_to_saved_model, str),
        )
    validation.ensure_not_empty((path_to_saved_model, ))

    #_n_gram_trie = 'encoded_text', 'n_gram_frequencies', 'n_grams', 'size', 'uni_grams'
    _n_gram_trie = {
        'encoded_text': model._n_gram_trie.encoded_text,
        'n_gram_frequencies': model._n_gram_trie.n_gram_frequencies,
        'n_grams': model._n_gram_trie.n_grams,
        'size': model._n_gram_trie.size,
        'uni_grams': model._n_gram_trie.uni_grams,
        }

    #_word_storage = 'storage', 'reversed_storage'
    _word_storage = {
        'storage': model._word_storage.storage,
        'reversed_storage': model._word_storage.reversed_storage,
        }

    model_dict = {
        'name': f'{type(model).__name__}',
        'data': {
            '_n_gram_trie' : _n_gram_trie,
            '_word_storage': _word_storage,
        }
    }

    # if *_n_gram_tries
    if model_dict['name'] == 'BackOffGenerator':
        _n_gram_tries = []

        for trie in model._n_gram_tries:
            _n_gram_trie = {
                'encoded_text': trie.encoded_text,
                'n_gram_frequencies': trie.n_gram_frequencies,
                'n_grams': trie.n_grams,
                'size': trie.size,
                'uni_grams': trie.uni_grams,
                }
            _n_gram_tries.append(_n_gram_trie)

        model_dict['data']['_n_gram_tries'] = _n_gram_tries

    with open(path_to_saved_model, 'w') as file:
        pprint(model_dict, stream=file, compact=True)


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    validation.ensure_type((path_to_saved_model, str))
    validation.ensure_not_empty((path_to_saved_model, ))

    with open(path_to_saved_model, 'r') as file:
        model_dict = file.read()

    model_dict = ast.literal_eval(model_dict)

    _n_gram_trie = NGramTrie(
        model_dict['data']['_n_gram_trie']['size'],
        model_dict['data']['_n_gram_trie']['encoded_text'],
        )
    _n_gram_trie.n_gram_frequencies = model_dict['data']['_n_gram_trie']['n_gram_frequencies']
    _n_gram_trie.n_grams = model_dict['data']['_n_gram_trie']['n_grams']
    _n_gram_trie.uni_grams = model_dict['data']['_n_gram_trie']['uni_grams']

    _word_storage = WordStorage()
    _word_storage.storage = model_dict['data']['_word_storage']['storage']
    _word_storage.reversed_storage = model_dict['data']['_word_storage']['reversed_storage']

    if model_dict['name'] == 'NGramTextGenerator':
        generator = NGramTextGenerator(_word_storage, _n_gram_trie)

    elif model_dict['name'] == 'LikelihoodBasedTextGenerator':
        generator = LikelihoodBasedTextGenerator(_word_storage, _n_gram_trie)

    elif model_dict['name'] == 'BackOffGenerator':
        tries = []
        for trie in model_dict['data']['_n_gram_tries']:
            _n_gram_trie = NGramTrie(
                trie['size'],
                trie['encoded_text'],
                )
            _n_gram_trie.n_gram_frequencies = trie['n_gram_frequencies']
            _n_gram_trie.n_grams = trie['n_grams']
            _n_gram_trie.uni_grams = trie['uni_grams']
            tries.append(_n_gram_trie)

        generator = BackOffGenerator(_word_storage, _n_gram_trie, *tries)

    return generator
