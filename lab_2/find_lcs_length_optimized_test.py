"""
Tests find_lcs_optimized function
"""

import time
import unittest
from lab_2.main import find_lcs_length, find_lcs_length_optimized


class FindLcsOptimizedTest(unittest.TestCase):
    """
    Checks for find_lcs_optimized function
    """

    def test_find_lcs_length_optimized_works_faster(self):
        """
        Tests find_lcs_optimized function
            can work faster than find_lcs_length function
        """
        sentence_first = ('the', 'dog', 'is', 'running', 'here')
        sentence_second = ('a', 'boy', 'plays', 'with', 'ball')
        plagiarism_threshold = 0.3

        start_time = time.time()
        find_lcs_length(sentence_first, sentence_second, plagiarism_threshold)
        end_time = time.time()

        start_time_second = time.time()
        find_lcs_length_optimized(list(sentence_first), list(sentence_second))
        end_time_second = time.time()

        actual_first = end_time - start_time
        actual_second = end_time_second - start_time_second
        self.assertGreater(actual_first, actual_second)
