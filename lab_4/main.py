"""
Lab 4
"""
import re
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    tokens = []
    sentences = re.split(r'[.!?][ \n]', text)
    for sentence in sentences:
        sentence_tokens = []
        for word in sentence.lower().split():
            if not word.isalpha():
                word = ''.join(filter(str.isalpha, word))
            if word:
                sentence_tokens.append(word)
        if sentence_tokens:
            sentence_tokens.append('<END>')
            tokens.extend(sentence_tokens)
    return tuple(tokens)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or not word:
            raise ValueError
        if word not in self.storage:
            self.storage[word] = len(self.storage)
        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or not word:
            raise ValueError
        if word not in self.storage:
            raise KeyError
        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int) or isinstance(word_id, bool):
            raise ValueError
        if word_id not in self.storage.values():
            raise KeyError
        for word, identifier in self.storage.items():
            if identifier == word_id:
                return word

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError
        for token in corpus:
            self._put_word(token)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError
    return tuple(storage.get_id(token) for token in text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if (not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1 or
                not all(isinstance(i, int) for i in context) or any(isinstance(i, bool) for i in context)):
            raise ValueError
        for n_gram, frequency in sorted(self._n_gram_trie.n_gram_frequencies.items(), key=lambda i: i[1], reverse=True):
            if n_gram[:-1] == context:
                return n_gram[-1]
        return sorted(self._n_gram_trie.uni_grams.items(), key=lambda i: i[1], reverse=True)[0][0][0]

    def _generate_sentence(self, context: tuple) -> tuple:
        if (not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1 or
                not all(isinstance(i, int) for i in context) or any(isinstance(i, bool) for i in context)):
            raise ValueError
        end_id = self._word_storage.storage['<END>']
        generated_sentence = list(context)
        while end_id not in generated_sentence and len(generated_sentence) < 20 + len(context):
            generated_sentence.append(self._generate_next_word(tuple(generated_sentence[-len(context):])))
        if end_id not in generated_sentence:
            generated_sentence.append(end_id)
        return tuple(generated_sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if (not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1 or
                not all(isinstance(i, int) for i in context) or any(isinstance(i, bool) for i in context) or
                not isinstance(number_of_sentences, int) or isinstance(number_of_sentences, bool)):
            raise ValueError
        generated_text = list(self._generate_sentence(context))
        for _ in range(number_of_sentences - 1):
            new_context = generated_text[-len(context):]
            while len(new_context) < len(context) * 2:
                new_context.append(self._generate_next_word(tuple(new_context[-len(context):])))
            new_context = tuple(new_context[-len(context):])
            generated_text.extend(list(self._generate_sentence(new_context)))
        return tuple(generated_text)


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if (not isinstance(word, int) or isinstance(word, bool) or not isinstance(context, tuple) or
                len(context) != self._n_gram_trie.size - 1 or not all(isinstance(i, int) for i in context) or
                any(isinstance(i, bool) for i in context)):
            raise ValueError
        context_frequency = 0
        for n_gram, frequency in self._n_gram_trie.n_gram_frequencies.items():
            if n_gram[:-1] == context:
                context_frequency += frequency
        likelihood = (self._n_gram_trie.n_gram_frequencies.get(tuple(list(context) + [word]), 0) /
                      context_frequency) if context_frequency else 0
        return likelihood

    def _generate_next_word(self, context: tuple) -> int:
        if (not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1 or
                not all(isinstance(i, int) for i in context) or any(isinstance(i, bool) for i in context) or
                any(i >= len(self._word_storage.storage) for i in context)):
            raise ValueError
        max_likelihood = 0
        next_word_id = 0
        for word_id in self._word_storage.storage.values():
            likelihood = self._calculate_maximum_likelihood(word_id, context)
            if likelihood > max_likelihood:
                max_likelihood = likelihood
                next_word_id = word_id
        if not max_likelihood:
            next_word_id = sorted(self._n_gram_trie.uni_grams.items(), key=lambda i: i[1], reverse=True)[0][0][0]
        return next_word_id


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple):
        raise ValueError
    text = []
    end_id = storage.storage['<END>']
    for i in range(encoded_text.count(end_id)):
        text.append([])
    sentence_num = 0
    for word_id in encoded_text:
        word = storage.get_word(word_id)
        if word != '<END>':
            text[sentence_num].append(word)
        else:
            text[sentence_num][0] = text[sentence_num][0].capitalize()
            text[sentence_num] = ' '.join(text[sentence_num])
            sentence_num += 1
    return tuple(text)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass
