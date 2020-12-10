# pylint: skip-file
"""
Tests for NGramTextGenerator class
"""

import unittest
from lab_4.ngrams.ngram_trie import NGramTrie


class NGramTrieTest(unittest.TestCase):
    """
    checks for NGramTextGenerator class.
    """

    def test_ngram_trie_instance_creation(self):
        """
        Checks that class creates correct instance
        """
        corpus = (1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 1, 2, 3, 10, 11, 5, 6, 7, 8, 12, 5, 13, 7, 8, 12, 11, 5)
        instance = NGramTrie(2, corpus)
        self.assertEqual(2, instance.size)

    def test_ngram_trie_unigrams(self):
        """
        Checks that class creates correct unigrams
        """
        corpus = (1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 1, 2, 3, 10, 11, 5, 6, 7, 8, 12, 5, 13, 7, 8, 12, 11, 5)
        instance = NGramTrie(2, corpus)
        unigrams = {(1,): 2, (2,): 2, (3,): 2, (4,): 1, (5,): 5, (6,): 2, (7,): 3,
                    (8,): 3, (9,): 1, (10,): 1, (11,): 2, (12,): 2, (13,): 1}
        self.assertEqual(unigrams, instance.uni_grams)

    def test_ngram_trie_freqs(self):
        """
        Checks that class creates correct freqs
        """
        corpus = (1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 1, 2, 3, 10, 11, 5, 6, 7, 8, 12, 5, 13, 7, 8, 12, 11, 5)
        instance = NGramTrie(2, corpus)
        freqs = {(1, 2): 2, (2, 3): 2, (3, 4): 1, (4, 5): 1, (5, 6): 2,
                 (6, 7): 2, (7, 8): 3, (8, 9): 1, (9, 5): 1, (5, 1): 1,
                 (3, 10): 1, (10, 11): 1, (11, 5): 2, (8, 12): 2,
                 (12, 5): 1, (5, 13): 1, (13, 7): 1, (12, 11): 1}

        self.assertEqual(freqs, instance.n_gram_frequencies)
