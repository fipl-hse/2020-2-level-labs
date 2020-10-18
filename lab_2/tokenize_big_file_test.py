"""
Tests tokenize_big_file function
"""

import unittest
import timeit
from memory_profiler import memory_usage
from lab_2.main import tokenize_big_file, tokenize_by_lines


class TokenizeBigFileTest(unittest.TestCase):
    """
    Checks for tokenize_big_file function
    """

    def test_tokenize_big_file_ideal_case(self):
        """
        Tests that tokenize_big_fie
            works just fine and not fails with big text
        """
        actual = tokenize_big_file('lab_2/data.txt')
        self.assertTrue(actual)

    def test_tokenize_big_file_quickest_time(self):
        """
        Tests that tokenize_big_file
            works faster than  time reference
        """
        start_time = timeit.default_timer()
        tokenize_big_file('lab_2/data.txt')
        end_time = timeit.default_timer()

        expected = 0.876659336000003 + (0.876659336000003 * 0.1)
        actual = end_time - start_time
        print(f'Actual tokenize_big_file function running time is: {actual}')
        print(f'Reference tokenize_big_file function time is: {expected}')
        self.assertGreater(expected, actual)

    def test_tokenize_big_file_lowest_memory(self):
        """
        Tests that tokenize_big_file
            works efficiently than given memory reference
        """
        expected = 64.22135416666667 + (64.22135416666667 * 0.1)
        actual_memory = memory_usage((tokenize_big_file, ('lab_2/data.txt',)),
                                     interval=2)
        actual = sum(actual_memory)/len(actual_memory)

        print(f'Actual tokenize_big_file function memory consuming is: {actual}')
        print(f'Reference tokenize_big_file function memory consuming is: {expected}')
        self.assertGreater(expected, actual)

    @unittest.skip
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
        print(f"Not optimized: {mean_memory_not_optimized}")
        print(f"Optimized: {mean_memory_optimized}")
        self.assertGreater(mean_memory_not_optimized, mean_memory_optimized)
