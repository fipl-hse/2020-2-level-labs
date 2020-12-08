"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie


SENTENCE_END = "<END>"


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    if not text:
        return tuple()
    
    separators = ".?!,(){}[]<>\\/@#$%^&*-+:;\"'`"
    sentence_endings = separators[:2]
    raw_tokens = text.lower().split()
    tokens = []
    for token in raw_tokens:
        correct_token = ''.join([letter for letter in token if letter not in separators])
        if correct_token:
            tokens.append(correct_token)
        if token[-1] in sentence_endings:
            tokens.append(SENTENCE_END)

    if not tokens:
        return tuple()

    if tokens[-1] != SENTENCE_END:
        tokens.append(SENTENCE_END)

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
        for word, _ in self.storage.items():
            if _ == word_id:
                return word

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError
        for token in corpus:
            self._put_word(token)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError
    storage.update(text)
    encoded_text = []
    for token in text:
        encoded_text.append(storage.get_id(token))
    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie
        self.context_size = self._n_gram_trie.size - 1

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) != self.context_size:
            raise ValueError
        contextual_n_grams = {
            n_gram: freq for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items()
            if n_gram[:self.context_size] == context
        }

        if not contextual_n_grams:
            return sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)[0][0]

        top_contextual_n_gram = sorted(contextual_n_grams.items(), key=lambda item: item[1])[0][0]
        return top_contextual_n_gram[-1]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or len(context) != self.context_size:
            raise ValueError
        generated_sentence = []
        generation_context = context
        end = self._word_storage.get_id(SENTENCE_END)

        generated_sentence.append(context)

        for _ in range(20):
            if _ > 0:
                generation_context = generated_sentence[-self.context_size:]
            next_word = self._generate_next_word(tuple(generation_context))
            generated_sentence.append(next_word)
            if next_word == end:
                break

        if generated_sentence[-1] != end:
            generated_sentence.append(end)

        return tuple(generated_sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if (
            not isinstance(context, tuple) or
            not isinstance(number_of_sentences, int) or
            isinstance(number_of_sentences, bool)
        ):
            raise ValueError

        generated_sentences = []
        generation_context = context

        for _ in range(number_of_sentences):
            #print(generation_context, "i =", _)
            if _ != 0:
                generation_context = generated_sentences[-1][-self.context_size:]
            generated_sentences.append(self._generate_sentence(generation_context))

        generated_text = [word for sentence in generated_sentences for word in sentence if isinstance(word, int)]
        return tuple(list(context) + generated_text)


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
