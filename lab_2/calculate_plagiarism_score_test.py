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
        lcs_matrix = 4
        suspicious_sentence_tokens = ('the', 'cat', 'is', 'sleeping')

        expected = 1
        actual = calculate_plagiarism_score(lcs_matrix, suspicious_sentence_tokens)
        self.assertEqual(expected, actual)

    def test_calculate_plagiarism_score_min(self):
        """
        Tests that calculate_plagiarism_score function
            can generate min plagiarism correctly
        """
        lcs_matrix = 0
        suspicious_sentence_tokens = ('the', 'cat', 'is', 'sleeping')

        expected = 0
        actual = calculate_plagiarism_score(lcs_matrix, suspicious_sentence_tokens)
        self.assertEqual(expected, actual)

    def test_calculate_plagiarism_score_incorrect_lcs_inputs(self):
        """
        Tests that calculate_plagiarism_score function
            can handle incorrect lcs_matrix inputs
        """

    def test_calculate_plagiarism_score_template(self):
        """
        Tests that calculate_plagiarism_score function
            can handle ...
        """
