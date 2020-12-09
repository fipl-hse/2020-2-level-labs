"""
Lab 4
"""
import re
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    sents = re.split(r'[.?!]', text)
    tokenized_sent = []

    for sent in sents:
        tokens = re.sub(r'[^a-z \n]', '', sent.lower()).split()

        if tokens:
            tokenized_sent += tokens + ['<END>']

    return tuple(tokenized_sent)


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
        if not isinstance(word_id, int):
            raise ValueError

        for key, value in self.storage.items():
            if value == word_id:
                return key

        raise KeyError

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError

        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError

    encoded_text = [storage.get_id(word) for word in text]

    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        ctxt_n_grams = {}
        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if context == n_gram[:self._n_gram_trie.size - 1]:
                ctxt_n_grams[n_gram] = freq

        if not ctxt_n_grams:
            finding_top_word = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
            return finding_top_word[0][0]

        finding_top_context_n_gram = sorted(ctxt_n_grams, key=ctxt_n_grams.get, reverse=True)
        return finding_top_context_n_gram[0][-1]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        sent_ctxt = []
        sent_ctxt.extend(list(context))
        counter = 0
        while counter < 20:
            counter += 1
            sent_ctxt.append(self._generate_next_word(tuple(sent_ctxt[-len(context):])))
            if sent_ctxt[-1] == self._word_storage.storage['<END>']:
                break
        else:
            sent_ctxt.append(self._word_storage.storage['<END>'])

        return tuple(sent_ctxt)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int) \
                or isinstance(number_of_sentences, bool):
            raise ValueError

        text = []
        while number_of_sentences:
            number_of_sentences -= 1
            new_sent = self._generate_sentence(context)

            if new_sent[len(context) - 1] == self._word_storage.storage['<END>']:
                new_sent = new_sent[len(context):]
            text.extend(new_sent)
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
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple) or not encoded_text:
        raise ValueError

    decoded_text = [[]]

    for encoded_word in encoded_text:
        decoded_word = storage.get_word(encoded_word)
        if decoded_word == '<END>':
            decoded_text.append([])
        else:
            decoded_text[-1].append(decoded_word)

    decoded_text = [sentence[0][0].upper() + sentence[0][1:] + ' ' + ' '.join(sentence[1:])
                    for sentence in decoded_text if sentence]

    return tuple(decoded_text)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

