# pylint: skip-file
"""
Tests create_diff_report function
"""

import unittest
from lab_2.main import create_diff_report, accumulate_diff_stats


class CreateDiffReportTest(unittest.TestCase):
    """
    Checks for create_diff_report function
    """

    @unittest.skip('')
    def test_create_diff_report_ideal(self):
        """
        Tests that create_diff_report function
            can handle ideal input case
        """
        original_text_tokens = (('i', 'have', 'a', 'cat'),
                                ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur'))
        suspicious_text_tokens = (('i', 'have', 'a', 'cat'),
                                  ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur'))
        accumulated_diff_stats = accumulate_diff_stats(original_text_tokens, suspicious_text_tokens)

        expected = open('lab_2/diff_report_example.txt', 'r', errors='coerce').read().split()
        actual = create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats).split()
        self.assertEqual(expected, actual)
        self.assertEqual(len(expected), len(actual))


if __name__ == "__main__":
    unittest.main()
