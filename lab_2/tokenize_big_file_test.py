"""
Tests tokenize_big_file function
"""

import unittest
from memory_profiler import memory_usage
from lab_2.main import tokenize_big_file, tokenize_by_lines


class TokenizeBigFileTest(unittest.TestCase):
    """
    Checks for tokenize_big_file function
    """

    def test_tokenize_big_file_ideal(self):
        """
        Tests that tokenize_big_file function
            can handle simple ideal case
        """
        with open('lab_2/tokenize_test_example.txt', 'r', encoding='utf-8') as file_to_read:
            data = file_to_read.read()

        memory_not_optimized = memory_usage((tokenize_by_lines, (data, )), interval=2)
        mean_memory_not_optimized = sum(memory_not_optimized)/len(memory_not_optimized)

        memory_optimized = memory_usage((tokenize_big_file,
                                         ('lab_2/tokenize_test_example.txt',)), interval=2)
        mean_memory_optimized = sum(memory_optimized)/len(memory_optimized)
        self.assertGreater(mean_memory_not_optimized, mean_memory_optimized)
