# pylint: skip-file
"""
Tests for NGramTextGenerator class
"""

import unittest
from lab_4.ngrams.ngram_trie import NGramTrie


class NGramTrieTest(unittest.TestCase):

    def test_ngram_trie_instance_creation(self):
        """
        check is instance created by tested class is correct
        """
        corpus = (1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 1, 2, 3, 10, 11, 5, 6, 7, 8, 12, 5, 13, 7, 8, 12, 11, 5)
        instance = NGramTrie(2, corpus)
        self.assertEqual(2, instance.size)
