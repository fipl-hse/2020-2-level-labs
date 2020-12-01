"""
Lab 4
"""
import re
from lab_4.ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    list_tokens = []
    for n_line_sentences in text.split('\n'):
        sentences = re.split('[!?.] ', n_line_sentences)
        for sentence in sentences:
            tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()
            print(tokens)
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
        if word_id not in self.storage.values():
            raise KeyError
        for word in self.storage:
            if self.storage[word] == word_id:
                return word

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
        if not isinstance(context, tuple) or not context or len(context) != self._n_gram_trie.size - 1:
            raise ValueError
        common_beg = []
        for n_gram in self._n_gram_trie.n_grams:
            if context == n_gram[:len(context)]:
                common_beg.append(n_gram)
        if common_beg:
            top = sorted(common_beg, key=self._n_gram_trie.n_gram_frequencies.get, reverse=True)
            return top[0][-1]
        top = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
        return top[0][0]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or not context:
            raise ValueError
        generated_sentence = []
        if self._word_storage.get_id('<END>') not in context:
            for word in context[:self._n_gram_trie.size-1]:
                generated_sentence.append(word)
        while self._word_storage.get_id('<END>') not in generated_sentence:
            generated_word = self._generate_next_word(context)
            context = context[:self._n_gram_trie.size-1] + (generated_word,)
            context = context[-(self._n_gram_trie.size - 1):]
            generated_sentence.append(generated_word)
            if len(generated_sentence) == 20:
                generated_sentence.append(self._word_storage.get_id('<END>'))
                return tuple(generated_sentence)
        return tuple(generated_sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int) or not context:
            raise ValueError
        generated_text = []
        while generated_text.count(self._word_storage.get_id('<END>')) != number_of_sentences:
            generated_sentence = self._generate_sentence(context)
            context = generated_sentence[-(self._n_gram_trie.size - 1):]
            generated_text.extend(list(generated_sentence))
        return tuple(generated_text)


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if not isinstance(context, tuple) or not isinstance(word, int) or not context\
                or len(context) != self._n_gram_trie.size - 1:
            raise ValueError
        appearing = 0
        for n_gram in self._n_gram_trie.n_grams:
            if context == n_gram[:len(context)]:
                appearing += 1
        if appearing == 0 or context + (word, ) not in self._n_gram_trie.n_gram_frequencies:
            return 0.0
        return self._n_gram_trie.n_gram_frequencies[context + (word, )] / appearing

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or not context or len(context) != self._n_gram_trie.size - 1:
            raise ValueError
        for word in context:
            if word not in self._word_storage.storage.values():
                raise ValueError
        likelihood_dict = {}
        for word in self._word_storage.storage.values():
            likelihood_dict[word] = self._calculate_maximum_likelihood(word, context)
        if likelihood_dict:
            top = sorted(likelihood_dict, key=likelihood_dict.get, reverse=True)
            return top[0]
        top = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
        return top[0][0]


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)
        self._n_gram_tries = (n_gram_trie, ) + args

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or not context:
            raise ValueError
        for word in context:
            if word not in self._word_storage.storage.values():
                raise ValueError
        trie_size_max = []
        for trie in self._n_gram_tries:
            trie_size_max.append(trie.size)
            common_beg = []
            for n_gram in trie.n_grams:
                if n_gram[:trie.size-1] == context[:trie.size-1]:
                    common_beg.append(n_gram)
            if common_beg:
                top = sorted(common_beg, key=trie.n_gram_frequencies.get, reverse=True)
                return top[0][-1]
        if not min(trie_size_max) - 1 <= len(context) <= max(trie_size_max) - 1:
            raise ValueError
        top = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
        return top[0][0]


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple):
        raise ValueError
    sentence = []
    sentences = []
    for encoded_word in encoded_text:
        if encoded_word != storage.get_id('<END>'):
            if len(sentence) == 0:
                word = storage.get_word(encoded_word)
                sentence.append(word[0].upper() + word[1:])
            else:
                sentence.append(storage.get_word(encoded_word))
        else:
            sentences.append(' '.join(sentence))
            sentence = []
    return tuple(sentences)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    if not isinstance(model, NGramTextGenerator) or not isinstance(path_to_saved_model, str):
        raise ValueError


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    if not isinstance(path_to_saved_model, str):
        raise ValueError
