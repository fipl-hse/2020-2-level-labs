"""
Tests calculate_text_plagiarism_score function
"""

import unittest
from unittest.mock import patch
from lab_2.main import calculate_text_plagiarism_score


class CalculateTextPlagiarismScoreTest(unittest.TestCase):
    """
    Checks for calculate_text_plagiarism_score function
    """

    def test_calculate_text_plagiarism_score_ideal(self):
        """
        Tests that calculate_text_plagiarism_score function
            can handle simple ideal input case
        """
        original_text_tokens = ()
        suspicious_text_tokens = ()
        plagiarism_threshold = 0.3

        expected = 9
        actual = 0
        self.assertEqual(expected, actual)

    def test_calculate_text_plagiarism_score_template(self):
        """
        Tests that calculate_text_plagiarism_score function
            can handle ...
        """

    def test_calculate_text_plagiarism_score_template(self):
        """
        Tests that calculate_text_plagiarism_score function
            can handle ...
        """



