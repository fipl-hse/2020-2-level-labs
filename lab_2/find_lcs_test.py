"""
Tests find_lcs function
"""

import unittest
from lab_2.main import find_lcs


class FindLcsTest(unittest.TestCase):
    """
    Checks for find_lcs function
    """

    def test_find_lcs_ideal_case(self):
        """
        Tests that find lcs function
            can handle ideal case
        """
        first_sentence = ('the', 'dog', 'is', 'running')
        second_sentence = ('the', 'cat', 'is', 'sleeping')
        lcs_matrix = [[1, 1, 1, 1],
                      [1, 1, 1, 1],
                      [1, 1, 2, 2],
                      [1, 1, 2, 2]]

        expected = ('the', 'is')
        actual = find_lcs(first_sentence, second_sentence, lcs_matrix)
        self.assertEqual(expected, actual)

    def test_find_lcs_no_lcs(self):
        """
        Tests that find lcs function
            can handle sentences with lcs equal to zero
        """
        first_sentence = ('the', 'dog', 'is', 'running')
        second_sentence = ('a', 'cat', 'was', 'sleeping')
        lcs_matrix = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        expected = ()
        actual = find_lcs(first_sentence, second_sentence, lcs_matrix)
        self.assertEqual(expected, actual)

    def test_find_lcs_reversed_behaviour(self):
        """
        Tests that find lcs function
            can handle the same params mixed
        """
        first_sentence = ('the', 'cat', 'is', 'sleeping')
        second_sentence = ('the', 'dog', 'is', 'sleeping')
        lcs_matrix = [[1, 1, 1, 1],
                      [1, 1, 1, 1],
                      [1, 1, 2, 2],
                      [1, 1, 2, 3]]

        expected = ('the', 'is', 'sleeping')
        actual = find_lcs(first_sentence, second_sentence, lcs_matrix)
        actual_reversed = find_lcs(second_sentence, first_sentence, lcs_matrix)
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_reversed)

    def test_find_lcs_empty_sentence(self):
        """
        Tests that find lcs function
            can handle empty sentence inputs
        """
        patches_sentence = ('the', 'cat', 'is', 'sleeping')
        empty_sentence = ()
        lcs_matrix = []

        expected = ()
        actual = find_lcs(empty_sentence, patches_sentence, lcs_matrix)
        actual_reversed = find_lcs(patches_sentence, empty_sentence, lcs_matrix)
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_reversed)

    def test_find_lcs_empty_lcs_matrix(self):
        """
        Tests that find lcs function
            can handle empty lcs_matrix param
        """
        patches_sentence = ('the', 'cat', 'is', 'sleeping')
        lcs_matrix = []

        expected = ()
        actual = find_lcs(patches_sentence, patches_sentence, lcs_matrix)
        self.assertEqual(expected, actual)

    def test_find_lcs_incorrect_sentence_inputs(self):
        """
        Tests that find lcs function
            can handle incorrect sentence inputs appropriately
        """
        patches_lcs_matrix = [[0, 0],
                              [0, 0]]
        patches_sentence = ('the', 'dog')
        bad_inputs = [[], {}, '', 9.22, -1, 0, -6, None, True, (None, None)]

        expected = ()
        for bad_input in bad_inputs:
            actual = find_lcs(bad_input, patches_sentence, patches_lcs_matrix)
            actual_second = find_lcs(patches_sentence, bad_input, patches_lcs_matrix)
            self.assertEqual(expected, actual)
            self.assertEqual(expected, actual_second)

    def test_find_lcs_incorrect_lcs_matrix_inputs(self):
        """
        Tests that find lcs function
            can handle incorrect matrix inputs appropriately
        """
        patches_sentence = ('the', 'dog')
        bad_inputs = [{}, '', 9.22, -1, 0, -6, None, True, (None, None), [None], [[None, None]]]

        expected = ()
        for bad_input in bad_inputs:
            actual = find_lcs(patches_sentence, patches_sentence, bad_input)
            self.assertEqual(expected, actual)

    def test_find_lcs_check_output(self):
        """
        Tests that find lcs function
            can generate correct output format according to specs
        """
        first_sentence = ('the', 'cat', 'is', 'sleeping')
        second_sentence = ('the', 'dog', 'is', 'sleeping')
        lcs_matrix = [[1, 1, 1, 1],
                      [1, 1, 1, 1],
                      [1, 1, 2, 2],
                      [1, 1, 2, 3]]

        actual = find_lcs(first_sentence, second_sentence, lcs_matrix)
        passed = True
        for word in actual:
            if not word.isalpha():
                passed = False
                break
        self.assertTrue(passed)

    def test_find_lcs_different_size(self):
        """
        Tests that find lcs function
            can handle different sized sentences
        """
        lcs_matrix = [[1, 1, 1, 1],
                      [1, 1, 1, 1],
                      [1, 1, 1, 1]]
        sentence_first = ('the', 'dog', 'sleeps')
        sentence_second = ('the', 'cat', 'is', 'sleeping')

        expected = ('the',)
        actual = find_lcs(sentence_first, sentence_second, lcs_matrix)
        self.assertEqual(expected, actual)

    def test_find_lcs_with_incorrect_matrix_provided(self):
        """
        Tests that find lcs function
            can check lcs_matrix matches given sentences
            NB! So the first element of lcs_matrix should be
                equal to 1 or 0, otherwise - empty tuple
        """
        lcs_matrix = [[1000, 1, 1, 1],
                      [1, 1, 1, 1],
                      [1, 1, 1, 1]]
        sentence_first = ('the', 'dog', 'sleeps')
        sentence_second = ('the', 'cat', 'is', 'sleeping')

        expected = ()
        actual = find_lcs(sentence_first, sentence_second, lcs_matrix)
        self.assertEqual(expected, actual)

    def test_find_lcs_matrix_with_incorrect_matrix_shape(self):
        """
        Tests that find_lcs function
            can check lcs_matrix shape is incorrect due to given sentences
        """
        lcs_matrix = [[0, 0],
                      [0, 0]]
        sentence_first = ('the', 'dog', 'sleeps')
        sentence_second = ('the', 'cat', 'is', 'sleeping')

        expected = ()
        actual = find_lcs(sentence_first, sentence_second, lcs_matrix)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()