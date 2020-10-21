"""
Tests tokenize_big_file function
"""

import unittest
import timeit
from memory_profiler import memory_usage
from lab_2.main import tokenize_big_file


class TokenizeBigFileTest(unittest.TestCase):
    """
    Checks for tokenize_big_file function
    """

    def test_tokenize_big_file_ideal_case(self):
        """
        Tests that tokenize_big_fie
            works just fine and not fails with big text
        """
        reference_len = 36970273
        actual = tokenize_big_file('lab_2/data.txt')
        print(f"Actual tokenize_big_file function length: {len(actual)}")
        print(f"Reference tokenize_big_file function length: {reference_len}")
        self.assertTrue(actual)
        self.assertEqual(reference_len, len(actual))

    def test_tokenize_big_file_quickest_time(self):
        """
        Tests that tokenize_big_file
            works faster than  time reference
        """
        start_time = timeit.default_timer()
        tokenize_big_file('lab_2/data.txt')
        end_time = timeit.default_timer()

        expected = 17.614083574000006 * 1.1
        actual = end_time - start_time
        print(f'Actual tokenize_big_file function running time is: {actual}')
        print(f'Reference tokenize_big_file function time is: {expected}')
        self.assertGreater(expected, actual)

    def test_tokenize_big_file_lowest_memory(self):
        """
        Tests that tokenize_big_file
            works efficiently than given memory reference
        """
        expected = 224.9296875 * 1.1
        actual_memory = memory_usage((tokenize_big_file, ('lab_2/data.txt',)),
                                     interval=2)
        actual = sum(actual_memory)/len(actual_memory)

        print(f'Actual tokenize_big_file function memory consuming is: {actual}')
        print(f'Reference tokenize_big_file function memory consuming is: {expected}')
        self.assertGreater(expected, actual)
