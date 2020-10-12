# pylint: skip-file
"""
Tests create_diff_report function
"""

import io
import sys
import unittest.mock
from lab_2.main import create_diff_report, accumulate_diff_stats


class CreateDiffReportTest(unittest.TestCase):
    """
    Checks for create_diff_report function
    """

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

        captured_output = io.StringIO()
        sys.stdout = captured_output
        create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats)
        sys.stdout = sys.__stdout__

        expected = open('lab_2/diff_report_example.txt', 'r', errors='coerce').read()
        actual = captured_output.getvalue()
        self.assertEqual(expected, actual)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_create_diff_report_using_mock(self, mock_stdout):
        """
        Tests that create_diff_report function
            can handle ideal input case
        """
        original_text_tokens = (('i', 'have', 'a', 'cat'),
                                ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur'))
        suspicious_text_tokens = (('i', 'have', 'a', 'cat'),
                                  ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur'))
        accumulated_diff_stats = accumulate_diff_stats(original_text_tokens, suspicious_text_tokens)
        create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats)

        expected = open('lab_2/diff_report_example.txt', 'r', errors='coerce').read()
        actual = mock_stdout.getvalue()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
