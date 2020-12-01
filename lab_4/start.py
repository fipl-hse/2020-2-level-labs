"""
Text generator
"""

import unittest
from lab_4.ngrams.ngram_trie import NGramTrie
from lab_4.main import WordStorage, LikelihoodBasedTextGenerator, BackOffGenerator
from lab_4.main import encode_text, decode_text


class TestsForGenerators(unittest.TestCase):
    """
    checks for LikelihoodBasedTextGenerator class
    """

    def test_likelihood_generator_generate_sentence(self):
        """
        Checks that class creates correct sentence
        """
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')
        storage = WordStorage()
        storage.update(corpus)
        encoded = encode_text(storage, corpus)
        trie = NGramTrie(3, encoded)
        context = (storage.get_id('i'),
                   storage.get_id('have'),)

        first_generated = storage.get_id('have')
        last_generated = storage.get_id('<END>')

        generator = LikelihoodBasedTextGenerator(storage, trie)
        actual = generator._generate_sentence(context)
        self.assertEqual(actual[1], first_generated)
        self.assertEqual(actual[-1], last_generated)

    def test_likelihood_generator_generate_text_ideal(self):
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

        generator = LikelihoodBasedTextGenerator(storage, trie)

        context = (storage.get_id('bruno'),)

        text = generator.generate_text(context, 3)
        actual = decode_text(storage, text)
        self.assertEqual(actual, ('Bruno', 'His name is rex', 'His name is rex'))

    def test_backoff_generator_generate_sentence(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        four = NGramTrie(4, encoded)
        trie = NGramTrie(3, encoded)

        context = (storage.get_id('his'),
                   storage.get_id('name'),
                   storage.get_id('bruno'),)

        first_generated = storage.get_id('is')
        last_generated = storage.get_id('<END>')

        generator = BackOffGenerator(storage, trie, four)
        actual = generator._generate_sentence(context)
        self.assertEqual(actual[2], first_generated)
        self.assertEqual(actual[-1], last_generated)

    def test_backoff_generator_generate_text_ideal(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        five = NGramTrie(5, encoded)
        trie = NGramTrie(3, encoded)
        four = NGramTrie(4, encoded)

        context = (storage.get_id('his'),
                   storage.get_id('name'),
                   storage.get_id('is'),
                   storage.get_id('bruno'),)

        generator = BackOffGenerator(storage, five, trie, four)

        text = generator.generate_text(context, 3)
        actual = decode_text(storage, text)
        self.assertEqual(actual, ('His name is bruno', 'I have a dog too', 'His name is bruno'))
