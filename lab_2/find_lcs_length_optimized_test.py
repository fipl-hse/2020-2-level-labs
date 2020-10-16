"""
Tests find_lcs_optimized function
"""

import timeit
import unittest
from lab_2.main import find_lcs_length, find_lcs_length_optimized
from lab_2.tokenizer import tokenize
from memory_profiler import memory_usage


class FindLcsOptimizedTest(unittest.TestCase):
    """
    Checks for find_lcs_optimized function
    """

    def test_find_lcs_length_optimized_works_faster(self):
        """
        Tests find_lcs_length_optimized function
            can work faster than find_lcs_length function
        """
        sentence_first = ('the', 'dog', 'is', 'running', 'here')
        sentence_second = ('a', 'boy', 'plays', 'with', 'ball')
        plagiarism_threshold = 0.3

        start_time = timeit.default_timer()
        find_lcs_length(sentence_first, sentence_second, plagiarism_threshold)
        end_time = timeit.default_timer()
        not_optimized = end_time - start_time

        start_time_second = timeit.default_timer()
        find_lcs_length_optimized(sentence_first, sentence_second, plagiarism_threshold)
        end_time_second = timeit.default_timer()
        optimized = end_time_second - start_time_second

        self.assertGreater(not_optimized, optimized)

    def test_find_lcs_length_optimized_memory_consumption(self):
        """
        Tests that find_lcs_length_optimized function
            consumes less memory than find_lcs_length
        """
        with open('lab_2/tokenize_test_example.txt', 'r', encoding='utf-8') as file_to_read:
            data = file_to_read.read()
        patches_sentence = tuple(tokenize(data))
        plagiarism_threshold = 0.3

        memory_not_optimized = memory_usage((find_lcs_length,
                                             patches_sentence,
                                             patches_sentence,
                                             plagiarism_threshold), interval=2)
        mean_memory_not_optimized = sum(memory_not_optimized) / len(memory_not_optimized)

        memory_optimized = memory_usage((find_lcs_length_optimized,
                                         patches_sentence,
                                         patches_sentence,
                                         plagiarism_threshold), interval=2)
        mean_memory_optimized = sum(memory_optimized) / len(memory_optimized)
        self.assertGreater(mean_memory_not_optimized, mean_memory_optimized)
