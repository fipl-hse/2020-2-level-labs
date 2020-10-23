"""
Tests accumulate_diff_stats function
"""

import unittest
from unittest.mock import patch
from lab_2.main import accumulate_diff_stats, find_lcs_length, calculate_plagiarism_score, find_diff_in_sentence


class AccumulateDiffStatsTest(unittest.TestCase):
    """
    Checks for accumulate_diff_stats function
    """

    def test_accumulate_diff_stats_ideal(self):
        """
        Tests that accumulate_diff_stats function
            can handle simple ideal input
        """
        first_text = (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
        second_text = (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'paw'))

        expected = {
            'text_plagiarism': 0.875,
            'sentence_plagiarism': [1.0, 0.75],
            'sentence_lcs_length': [4, 3],
            'difference_indexes': [((), ()), ((3, 4), (3, 4))]
        }
        actual = accumulate_diff_stats(first_text, second_text)
        self.assertEqual(expected, actual)

    def test_accumulate_diff_stats_check_output(self):
        """
        Tests that accumulate_diff_stats function
            can generate correct correct output according to given specs
        """
        expected = {
            'text_plagiarism': 0.875,
            'sentence_plagiarism': [1.0, 0.75],
            'sentence_lcs_length': [4, 3],
            'difference_indexes': [((), ()), ((3, 4), (3, 4))]
        }
        text_first = (('i', 'have', 'a', 'cat'),
                      ('his', 'name', 'is', 'bruno'))
        text_second = (('i', 'have', 'a', 'cat'),
                       ('his', 'name', 'is', 'paw'))

        actual = accumulate_diff_stats(text_first, text_second)
        self.assertIn('text_plagiarism', actual)
        self.assertIn('sentence_plagiarism', actual)
        self.assertIn('sentence_lcs_length', actual)
        self.assertIn('difference_indexes', actual)
        self.assertEqual(expected['text_plagiarism'], actual['text_plagiarism'])
        self.assertEqual(expected['sentence_plagiarism'], actual['sentence_plagiarism'])
        self.assertEqual(expected['sentence_lcs_length'], actual['sentence_lcs_length'])
        self.assertEqual(expected['difference_indexes'], actual['difference_indexes'])

    @patch('lab_2.main.find_lcs_length', side_effect=find_lcs_length)
    def test_accumulate_diff_stats_calls_required_function(self, mock):
        """
        Tests that accumulate_diff_stats function
            can call required function
        """
        patches_text = (('i', 'have', 'a', 'cat'),
                        ('his', 'name', 'is', 'bruno'))

        accumulate_diff_stats(patches_text, patches_text)
        self.assertTrue(mock.called)

    @patch('lab_2.main.calculate_plagiarism_score', side_effect=calculate_plagiarism_score)
    def test_accumulate_diff_stats_calls_second_required_function(self, mock):
        """
        Tests that accumulate_diff_stats function
            can call required function
        """
        patches_text = (('i', 'have', 'a', 'cat'),
                        ('his', 'name', 'is', 'bruno'))

        accumulate_diff_stats(patches_text, patches_text)
        self.assertTrue(mock.called)

    @patch('lab_2.main.find_diff_in_sentence', side_effect=find_diff_in_sentence)
    def test_accumulate_diff_stats_calls_third_required_function(self, mock):
        """
        Tests that accumulate_diff_stats function
            can call required function
        """
        patches_text = (('i', 'have', 'a', 'cat'),
                        ('his', 'name', 'is', 'bruno'))

        accumulate_diff_stats(patches_text, patches_text)
        self.assertTrue(mock.called)


if __name__ == "__main__":
    unittest.main()