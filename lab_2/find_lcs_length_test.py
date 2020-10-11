"""
Tests find_lcs_length function
"""

import unittest
from unittest.mock import patch
from lab_2.main import find_lcs_length, fill_lcs_matrix


class FindLcsLengthTest(unittest.TestCase):
    """
    Checks for find_lcs_length function
    """

    def test_find_lcs_length_ideal(self):
        """
        Tests that find_lcs_matrix function
            can handle simple input case
        """
        expected = 2

        sentence_first = ('the', 'dog', 'is', 'running')
        sentence_second = ('the', 'cat', 'is', 'sleeping')
        plagiarism_threshold = 0.3

        actual = find_lcs_length(sentence_first, sentence_second, plagiarism_threshold)
        self.assertEqual(expected, actual)

    def test_find_lcs_length_complex(self):
        """
        Tests that find_lcs_length function
            can handle complex input case
        """
        expected = 5

        sentence_first = ('the', 'dog', 'is', 'running', 'inside', 'the', 'house')
        sentence_second = ('the', 'cat', 'is', 'sleeping', 'inside', 'the', 'house')
        plagiarism_threshold = 0.3

        actual = find_lcs_length(sentence_first, sentence_second, plagiarism_threshold)
        self.assertEqual(expected, actual)

    def test_find_lcs_length_different_sized_inputs(self):
        """
        Tests that find_lcs_length function
            can handle different sized token inputs
        """
        expected = 3

        sentence_first = ('the', 'dog', 'is', 'running', 'inside')
        sentence_second = ('the', 'cat', 'is', 'sleeping', 'inside', 'the', 'house')
        plagiarism_threshold = 0.3

        actual = find_lcs_length(sentence_first, sentence_second, plagiarism_threshold)
        actual_reversed = find_lcs_length(sentence_second, sentence_first, plagiarism_threshold)
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_reversed)

    def test_find_lcs_length_no_diff(self):
        """
        Tests that find_lcs_length function
            can handle fully different sentences
        """
        expected = 0

        sentence_first = ('the', 'dog', 'is', 'running', 'here')
        sentence_second = ('a', 'boy', 'plays', 'with', 'ball')
        plagiarism_threshold = 0.3

        actual = find_lcs_length(sentence_first, sentence_second, plagiarism_threshold)
        self.assertEqual(expected, actual)

    def test_find_lcs_length_empty_input(self):
        """
        Tests that find_lcs_length function
            can handle empty input params
        """
        expected = 0

        empty_sentence = ()
        patches_sentence = ('a', 'boy', 'plays', 'with', 'ball')

        actual = find_lcs_length(empty_sentence, patches_sentence)
        actual_reversed = find_lcs_length(patches_sentence, empty_sentence)
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_reversed)

    def test_find_lcs_length_reversed_behaviour(self):
        """
        Tests that find_lcs_length function
            can reverse input sentences params
        """
        expected = 2
        sentence_first = ('the', 'dog', 'is', 'running', 'inside', 'the', 'house')
        sentence_second = ('the', 'cat', 'is', 'sleeping', 'inside', 'the', 'house')

        actual = find_lcs_length(sentence_first, sentence_second)
        actual_reversed = find_lcs_length(sentence_second, sentence_first)
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_reversed)

    def test_find_lcs_length_output_check(self):
        """
        Tests that find_lcs_length function
            can generate correct output according to given params
        """
        sentence_first = ('the', 'dog', 'is', 'running', 'here')
        sentence_second = ('a', 'boy', 'plays', 'with', 'ball')
        plagiarism_threshold = 0.3

        actual = find_lcs_length(sentence_first, sentence_second, plagiarism_threshold)
        self.assertTrue(isinstance(actual, int))

    def test_find_lcs_length_incorrect_inputs(self):
        """
        Tests that find_lcs_length function
            can handle incorrect inputs
        """
        expected = -1
        bad_inputs = [[], {}, '', 9.22, -1, 0, -6, None, True, (None, None)]
        patches_sentence = ('the', 'dog', 'is', 'running')
        plagiarism_threshold = 0.3

        for bad_input in bad_inputs:
            actual = find_lcs_length(bad_input, patches_sentence, plagiarism_threshold)
            actual_reversed = find_lcs_length(patches_sentence, bad_input, plagiarism_threshold)
            self.assertEqual(expected, actual)
            self.assertEqual(expected, actual_reversed)

    def test_find_lcs_length_incorrect_threshold(self):
        """
        Tests that find_lcs_length function
            can handle incorrect threshold input
        """
        expected = -1
        bad_inputs = [[], {}, '', -1, -6.34, None, True, (None, None)]
        patches_sentence = ('the', 'dog', 'is', 'running')

        for bad_input in bad_inputs:
            actual = find_lcs_length(patches_sentence, patches_sentence, bad_input)
            self.assertEqual(expected, actual)

    @patch('main.fill_lcs_matrix', side_effect=fill_lcs_matrix)
    def test_find_lcs_length_calls_required_function(self, mock):
        """
        Tests that find_lcs_length function
            calls fill_lcs_matrix function
        """
        patches_sentence = ('the', 'dog', 'is', 'running')
        plagiarism_threshold = 0.3

        find_lcs_length(patches_sentence, patches_sentence, plagiarism_threshold)
        self.assertTrue(mock.called)


if __name__ == "__main__":
    unittest.main()
