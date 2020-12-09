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
        if not isinstance(word, str) or not word:
            raise ValueError
        if word not in self.storage:
            self.storage[word] = len(self.storage) + 1
        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or not word:
            raise ValueError
        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int) or not word_id:
            raise ValueError
        for word, w_id in self.storage.items():
            if word_id == w_id:
                return word
        raise KeyError


    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple) or (corpus and not isinstance(corpus[0], str)):
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
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError
        full_context = self.get_most_frequent_gram(context)
        if not full_context:
            return max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]
        return full_context[-1]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError
        sentence = list(context)
        for _ in range(20):
            sentence.append(self._generate_next_word(tuple(sentence[-(len(context)):])))
            if sentence[-1] == self._word_storage.storage['<END>']:
                break
        else:
            sentence.append(self._word_storage.storage['<END>'])
        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError
        sentences = []
        for _ in range(number_of_sentences):
            new_sent = self._generate_sentence(context)
            if new_sent[len(context) - 1] == self._word_storage.storage['<END>']:
                new_sent = new_sent[len(context):]
            sentences.extend(new_sent)
            context = tuple(sentences[-len(context):])
        return tuple(sentences)

    def get_most_frequent_gram(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or not context:
            return ()
        max_freq = 0
        full_context = ()
        for key, freq in self._n_gram_trie.n_gram_frequencies.items():
            if key[:len(context)] == context and freq > max_freq:
                max_freq = freq
                full_context = key
        return full_context



class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if not isinstance(word, int) or not isinstance(context, tuple) or \
                not (word,) in self._n_gram_trie.uni_grams or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        freq_context = 0.0
        for key, freq in self._n_gram_trie.n_gram_frequencies.items():
            if key[:len(context)] == context:
                freq_context += freq

        if freq_context:
            freq_context = self._n_gram_trie.n_gram_frequencies.get(tuple(list(context) + [word]), 0) / freq_context

        return freq_context

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size or \
                context[0] > len(self._word_storage.storage):
            raise ValueError
        max_freq = 0
        word = 0
        for value in self._word_storage.storage.values():
            frequency = self._calculate_maximum_likelihood(value, context)
            if frequency > max_freq:
                max_freq = frequency
                word = value
        if not max_freq:
            word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]
        return word



class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass

    def get_auxiliary_param(self):
        pass

def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple) or not encoded_text:
        raise ValueError
    text_raw = [[]]
    for word in encoded_text:
        real_word = storage.get_word(word)
        print(real_word)
        if real_word == '<END>':
            text_raw.append([])
        else:
            text_raw[-1].append(real_word)
    text_ready = [
        sentence[0][0].upper() + sentence[0][1:] + ' ' + ' '.join(sentence[1:])
        for sentence in text_raw if sentence
    ]
    return tuple(text_ready)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass

def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass
