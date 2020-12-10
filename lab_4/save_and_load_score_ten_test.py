# pylint: skip-file
"""
Tests for save and load model functions
"""

import unittest
from lab_4.main import WordStorage, encode_text, NGramTextGenerator, save_model, load_model
from lab_4.ngrams.ngram_trie import NGramTrie

@unittest.skip
class SaveModelTest(unittest.TestCase):
    """
    checks for save_model unction.
    """

    def test_save_model_ideal(self):
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

        save_model(generator, 'my_awesome_model')

        with open('my_awesome_model', 'r', encoding='utf-8') as file_to_read:
            data = file_to_read.read()
        self.assertTrue(data)

    def test_save_model_incorrect(self):
        bad_inputs = [(), [], 123, None, WordStorage]

        for bad_model in bad_inputs:
            self.assertRaises(ValueError, save_model, bad_model, 'my_awesome_model')

@unittest.skip
class LoadModelTest(unittest.TestCase):
    """
    checks for load_model unction.
    """

    def test_load_model_ideal(self):
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

        save_model(generator, 'my_awesome_model')
        loaded_model = load_model('my_awesome_model')

        self.assertEqual(generator._n_gram_trie.n_grams,
                         loaded_model._n_gram_trie.n_grams)
        self.assertEqual(len(generator._n_gram_trie.n_gram_frequencies),
                         len(loaded_model._n_gram_trie.n_gram_frequencies))
        for ngram, frequency in generator._n_gram_trie.n_gram_frequencies.items():
            self.assertTrue(ngram in loaded_model._n_gram_trie.n_gram_frequencies)
            self.assertEqual(frequency, loaded_model._n_gram_trie.n_gram_frequencies[ngram])

        self.assertEqual(len(generator._word_storage.storage),
                         len(loaded_model._word_storage.storage))
        for word, id_num in generator._word_storage.storage.items():
            self.assertTrue(word in loaded_model._word_storage.storage)
            self.assertEqual(id_num, loaded_model._word_storage.storage[word])
