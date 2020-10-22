"""
Tests find_lcs_optimized function
"""

import timeit
import unittest
from memory_profiler import memory_usage

from lab_2.main import find_lcs_length_optimized, tokenize_big_file


class FindLcsOptimizedTest(unittest.TestCase):
    """
    Checks for find_lcs_optimized function
    """

    def test_find_lcs_length_optimized_ideal_case(self):
        """
        Tests that find_lcs_length_optimized
            works just fine and not fails with big text
        """
        sentence_tokens_first_text = tokenize_big_file('lab_2/data.txt')[:30000]
        sentence_tokens_second_text = tokenize_big_file('lab_2/data_2.txt')[:30000]
        plagiarism_threshold = 0.0001
        actual = find_lcs_length_optimized(sentence_tokens_first_text,
                                           sentence_tokens_second_text,
                                           plagiarism_threshold)
        reference_lcs = 3899
        print(f"Actual find_lcs_length_optimized function lcs is {actual}")
        print(f"Reference find_lcs_length_optimized function lcs is {reference_lcs}")
        self.assertTrue(actual)
        self.assertEqual(reference_lcs, actual)

    def test_find_lcs_length_optimized_quickest_time(self):
        """
        Tests that find_lcs_length_optimized
            works faster than  time reference
        """
        reference = 353.6632048700001 * 1.1
        sentence_tokens_first_text = tokenize_big_file('lab_2/data.txt')[:30000]
        sentence_tokens_second_text = tokenize_big_file('lab_2/data_2.txt')[:30000]
        plagiarism_threshold = 0.0001

        start_time = timeit.default_timer()
        find_lcs_length_optimized(sentence_tokens_first_text,
                                  sentence_tokens_second_text,
                                  plagiarism_threshold)
        end_time = timeit.default_timer()
        actual = end_time - start_time

        print(f"Actual find_lcs_length_optimized function running time is: {actual}")
        print(f"Reference find_lcs_length_optimized function running time is: {reference}")
        self.assertGreater(reference, actual)

    def test_find_lcs_length_optimized_lowest_memory(self):
        """
        Tests that find_lcs_length_optimized
            works efficiently than given memory reference
        """
        reference = 65.69129527698863 * 1.1
        sentence_tokens_first_text = tokenize_big_file('lab_2/data.txt')[:30000]
        sentence_tokens_second_text = tokenize_big_file('lab_2/data_2.txt')[:30000]
        plagiarism_threshold = 0.0001

        actual_memory = memory_usage((find_lcs_length_optimized,
                                      (sentence_tokens_first_text,
                                       sentence_tokens_second_text,
                                       plagiarism_threshold)),
                                     interval=2)
        actual = sum(actual_memory)/len(actual_memory)

        print(f'Actual find_lcs_length_optimized function memory consuming is: {actual}')
        print(f'Reference find_lcs_length_optimized function memory consuming is: {reference}')
        self.assertGreater(reference, actual)
