# pylint: skip-file
"""
Tests decode_text function
"""

import unittest
from lab_4.main import encode_text, WordStorage, LikelihoodBasedTextGenerator, decode_text
from lab_4.ngrams.ngram_trie import NGramTrie


class DecodeCorpusTest(unittest.TestCase):
    """
    checks for decode_text function.
        Score 8 or above function
    """

    def test_decode_text_ideal(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        trie = NGramTrie(3, encoded)

        context = (storage.get_id('name'),
                   storage.get_id('is'),)
        end = storage.get_id('<END>')

        generator = LikelihoodBasedTextGenerator(storage, trie)

        to_decode = generator.generate_text(context, 2)
        self.assertEqual(to_decode[-1], end)

        expected = ('Name is rex', 'Her name is rex')
        actual = decode_text(storage, to_decode)
        self.assertEqual(expected, actual)

    def test_decode_text_incorrect_storage(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        trie = NGramTrie(3, encoded)

        context = (storage.get_id('name'),
                   storage.get_id('is'),)

        generator = LikelihoodBasedTextGenerator(storage, trie)

        to_decode = generator.generate_text(context, 2)

        bad_inputs = [(), [], 123, None, NGramTrie]

        for bad_storage in bad_inputs:
            self.assertRaises(ValueError, decode_text, bad_storage, to_decode)

    def test_decode_text_incorrect_sentences(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        bad_inputs = [[], 123, None, NGramTrie]

        for bad_decode in bad_inputs:
            self.assertRaises(ValueError, decode_text, storage, bad_decode)

    def test_decode_text_ideal_conditions(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        trie = NGramTrie(3, encoded)

        context = (storage.get_id('name'),
                   storage.get_id('is'),)

        generator = LikelihoodBasedTextGenerator(storage, trie)

        to_decode = generator.generate_text(context, 2)
        actual = decode_text(storage, to_decode)

        for sentence in actual:
            self.assertTrue('<END>' not in sentence)
            self.assertTrue(sentence[0].isupper())
            self.assertTrue(sentence[-1].isalpha())

    def test_end(self):
        """
             Checks that after decoding no end in result
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'cat', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        trie = NGramTrie(3, encoded)
        context = (storage.get_id('a'),
                   storage.get_id('cat'),)

        generator = LikelihoodBasedTextGenerator(storage, trie)

        to_decode = generator.generate_text(context, 1)
        actual = decode_text(storage, to_decode)
        expected = ('A cat',)
        self.assertEqual(expected, actual)
