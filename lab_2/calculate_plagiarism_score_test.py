"""
Tests calculate_plagiarism_score function
"""

import unittest
from lab_2.main import calculate_plagiarism_score


class CalculatePlagiarismScoreTest(unittest.TestCase):
    """
    Checks for calculate_plagiarism_score function
    """

    def test_calculate_plagiarism_score_ideal(self):
        """
        Tests that calculate_plagiarism_score function
            can handle ideal simple input
        """
        lcs_length = 3
        suspicious_sentence_tokens = ('the', 'cat', 'is', 'sleeping')
        expected = 0.75
        actual = calculate_plagiarism_score(lcs_length, suspicious_sentence_tokens)
        self.assertEqual(expected, actual)

    def test_calculate_plagiarism_score_max(self):
        """
        Tests that calculate_plagiarism_score function
            can generate max plagiarism correctly
        """
        lcs_length = 4
        suspicious_sentence_tokens = ('the', 'cat', 'is', 'sleeping')

        expected = 1.0
        actual = calculate_plagiarism_score(lcs_length, suspicious_sentence_tokens)
        self.assertEqual(expected, actual)

    def test_calculate_plagiarism_score_min(self):
        """
        Tests that calculate_plagiarism_score function
            can generate min plagiarism correctly
        """
        lcs_length = 0
        suspicious_sentence_tokens = ('the', 'cat', 'is', 'sleeping')

        expected = 0.0
        actual = calculate_plagiarism_score(lcs_length, suspicious_sentence_tokens)
        self.assertEqual(expected, actual)

    def test_calculate_plagiarism_score_incorrect_lcs_inputs(self):
        """
        Tests that calculate_plagiarism_score function
            can handle incorrect lcs_matrix inputs
        """
        bad_inputs = [[], {}, (), '', 9.22, -1, -6, None, True]
        patches_sentence = ('the', 'cat', 'is', 'sleeping')

        expected = -1
        for bad_input in bad_inputs:
            actual = calculate_plagiarism_score(bad_input, patches_sentence)
            self.assertEqual(expected, actual)

    def test_calculate_plagiarism_score_incorrect_sentence_input(self):
        """
        Tests that calculate_plagiarism_score function
            can handle incorrect suspicious_sentence_tokens inputs
        """
        patches_lcs_length = 0
        bad_inputs = [[], {}, (), 9.22, -1, 0, -6, None, True]

        expected = -1
        for bad_input in bad_inputs:
            actual = calculate_plagiarism_score(patches_lcs_length, bad_input)
            self.assertEqual(expected, actual)

    def test_calculate_plagiarism_score_incorrectly_filled_sentence(self):
        """
        Tests that calculate_plagiarism_score function
            can handle incorrectly filled sentence
        """
        patches_lcs_length = 2
        sentence = ('', '', None)

        expected = -1
        actual = calculate_plagiarism_score(patches_lcs_length, sentence)
        self.assertEqual(expected, actual)

    def test_calculate_plagiarism_score_empty_sentence(self):
        """
        Tests that calculate_plagiarism_score function
            can handle empty sentence input
        """
        patches_lcs_length = 2
        sentence = ()

        expected = 0.0
        actual = calculate_plagiarism_score(patches_lcs_length, sentence)
        self.assertEqual(expected, actual)

    def test_calculate_plagiarism_score_check_output(self):
        """
        Tests that calculate_plagiarism_score function
            can generate correct output according to given specs
        """
        lcs_length = 3
        suspicious_sentence_tokens = ('the', 'cat', 'is', 'sleeping')

        actual = calculate_plagiarism_score(lcs_length, suspicious_sentence_tokens)
        self.assertTrue(isinstance(actual, float))

    def test_calculate_plagiarism_score_different_lcs_length(self):
        """
        Tests that calculate_plagiarism_score function
            can handle bigger lcs_length than given sentence
        """
        lcs_length = 1000000
        suspicious_sentence_tokens = ('the', 'cat', 'is', 'sleeping')

        expected = -1
        actual = calculate_plagiarism_score(lcs_length, suspicious_sentence_tokens)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
