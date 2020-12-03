# pylint: skip-file
"""
Tests for NGramTextGenerator class
"""

import unittest
from lab_4.main import NGramTextGenerator, WordStorage, encode_text
from lab_4.ngrams.ngram_trie import NGramTrie


class NGramTextGeneratorTest(unittest.TestCase):
    """
    checks for NGramTextGenerator class.
        All tests should pass for score 6 or above
    """

    def test_ngram_text_generator_instance_creation(self):
        """
        Checks that class creates correct instance
        """
        word_storage = WordStorage()
        ngram = NGramTrie(2, ())

        generator = NGramTextGenerator(word_storage, ngram)
        self.assertEqual(generator._word_storage, word_storage)
        self.assertEqual(generator._n_gram_trie, ngram)

# --------------------------------------------------------------

    def test_ngram_text_generator_generate_next_word(self):
        """
        Checks that next word generates properly
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'i', 'have', 'a', 'bruno', 'cat', '<END>')
        word_storage = WordStorage()
        word_storage.update(corpus)
        encoded = encode_text(word_storage, corpus)
        ngram = NGramTrie(3, encoded)

        generator = NGramTextGenerator(word_storage, ngram)
        context = (word_storage.get_id('i'),
                   word_storage.get_id('have'))
        expected = word_storage.get_id('a')
        actual = generator._generate_next_word(context)
        self.assertEqual(expected, actual)

    def test_ngram_text_generator_generate_next_word_incorrect_context(self):
        """
        Checks that method throws error
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>')
        word_storage = WordStorage()
        word_storage.update(corpus)
        encoded = encode_text(word_storage, corpus)
        ngram = NGramTrie(3, encoded)

        generator = NGramTextGenerator(word_storage, ngram)
        bad_inputs = [[], {}, (3, ), None, 9, 9.34, True]  # (3, ) - it is incorrect sized ngram
        for bad_input in bad_inputs:
            self.assertRaises(ValueError, generator._generate_next_word, bad_input)

    def test_ngram_text_generator_generate_next_word_no_such_context(self):
        """
        Checks that next word generates properly if no context found
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>')
        word_storage = WordStorage()
        word_storage.update(corpus)

        encoded = encode_text(word_storage, corpus)

        ngram = NGramTrie(3, encoded)

        generator = NGramTextGenerator(word_storage, ngram)
        context = (word_storage.get_id('i'),
                   word_storage.get_id('name'),)  # there is no such context in ngrams, so return most frequent option
        expected_top_freq = word_storage.get_id('<END>')  # as it appears twice
        actual = generator._generate_next_word(context)
        self.assertEqual(expected_top_freq, actual)

# --------------------------------------------------------------------------------

    def test_ngram_text_generator_generate_sentence_properly(self):
        """
        generates correct output according to simple case
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>')
        word_storage = WordStorage()
        word_storage.update(corpus)
        encoded = encode_text(word_storage, corpus)
        trie = NGramTrie(2, encoded)
        context = (word_storage.get_id('i'), )

        end = word_storage.get_id('<END>')

        generator = NGramTextGenerator(word_storage, trie)
        actual = generator._generate_sentence(context)
        self.assertEqual(actual[-1], end)

    def test_ngram_text_generator_generate_sentence_ideal(self):
        """
        first and last generated words as expected
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')
        storage = WordStorage()
        storage.update(corpus)
        encoded = encode_text(storage, corpus)
        trie = NGramTrie(2, encoded)
        context = (storage.get_id('i'), )

        first_generated = storage.get_id('have')
        last_generated = storage.get_id('<END>')

        generator = NGramTextGenerator(storage, trie)
        actual = generator._generate_sentence(context)
        self.assertEqual(actual[1], first_generated)
        self.assertEqual(actual[-1], last_generated)

    def test_ngram_text_generator_generate_sentence_no_end(self):
        """
        should generate '<END>' anyway
        """
        corpus = ('i', 'have', 'a', 'cat', 'his', 'name', 'is', 'bruno', 'i', 'have', 'a', 'dog', 'too',
                  'his', 'name', 'is', 'rex', 'her', 'name', 'is', 'rex', 'too', '<END>')
        word_storage = WordStorage()
        word_storage.update(corpus)
        encoded = encode_text(word_storage, corpus)
        trie = NGramTrie(2, encoded)
        context = (word_storage.get_id('cat'), )

        generator = NGramTextGenerator(word_storage, trie)
        actual = generator._generate_sentence(context)

        expected = '<END>'
        actual = word_storage.get_word(actual[-1])
        self.assertEqual(expected, actual)

    def test_ngram_text_generator_throws_errors(self):
        """
        throws errors with bad inputs
        """
        bad_inputs = [[], {}, None, 9, 9.34, True]
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>')
        word_storage = WordStorage()
        word_storage.update(corpus)
        encoded = encode_text(word_storage, corpus)
        trie = NGramTrie(2, encoded)
        generator = NGramTextGenerator(word_storage, trie)

        for bad_input in bad_inputs:
            self.assertRaises(ValueError, generator._generate_sentence, bad_input)

# ---------------------------------------------------------------------------------

    def test_generate_text_ideal(self):
        """
        should generate simple case with three sentences out of small corpus
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        trie = NGramTrie(2, encoded)

        generator = NGramTextGenerator(storage, trie)

        context = (storage.get_id('bruno'),)
        end = storage.get_id('<END>')
        actual = generator.generate_text(context, 3)
        self.assertEqual(actual.count(end), 3)

    def test_text_generator_throws_errors(self):
        """
        throws errors with bad inputs
        """
        bad_inputs = [[], {}, None, 9, 9.34, True]
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>')
        word_storage = WordStorage()
        word_storage.update(corpus)
        encoded = encode_text(word_storage, corpus)
        trie = NGramTrie(2, encoded)
        generator = NGramTextGenerator(word_storage, trie)

        for bad_input in bad_inputs:
            self.assertRaises(ValueError, generator.generate_text, bad_input, 10)

# ---------------------------------------------------------------------------------

    def test_get_most_frequent_gram_ideal(self):
        """
        Checks that most frequent ngram gets properly
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'i', 'have', 'a', 'bruno', 'cat', '<END>')
        word_storage = WordStorage()
        word_storage.update(corpus)
        encoded = encode_text(word_storage, corpus)
        ngram = NGramTrie(3, encoded)

        generator = NGramTextGenerator(word_storage, ngram)
        context = (word_storage.get_id('i'),
                   word_storage.get_id('have'))
        expected = (word_storage.get_id('i'),
                    word_storage.get_id('have'),
                    word_storage.get_id('a'))
        actual = generator.get_most_frequent_gram(context)
        self.assertEqual(expected, actual)

    def test_get_most_frequent_gram_bad_inputs(self):
        """
        Checks that method returns empty tuple
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>')
        word_storage = WordStorage()
        word_storage.update(corpus)
        encoded = encode_text(word_storage, corpus)
        ngram = NGramTrie(3, encoded)
        expected = ()
        generator = NGramTextGenerator(word_storage, ngram)
        bad_inputs = [[], {}, (), None, 9, 9.34, True]
        for bad_input in bad_inputs:
            self.assertEqual(expected, generator.get_most_frequent_gram(bad_input))

    def test_get_most_frequent_gram_no_such_context(self):
        """
        Checks that returns empty tuple with no context in the corpus
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>')
        word_storage = WordStorage()
        word_storage.update(corpus)
        encoded = encode_text(word_storage, corpus)
        ngram = NGramTrie(3, encoded)
        generator = NGramTextGenerator(word_storage, ngram)

        context = (word_storage.get_id('i'),
                   word_storage.get_id('name'),)  # there is no such context in ngrams
        expected = ()
        actual = generator.get_most_frequent_gram(context)
        self.assertEqual(expected, actual)
