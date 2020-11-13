"""
Tests calculate_text_plagiarism_score function
"""

import unittest
from unittest.mock import patch
from lab_2.main import calculate_text_plagiarism_score, calculate_plagiarism_score


class CalculateTextPlagiarismScoreTest(unittest.TestCase):
    """
    Checks for calculate_text_plagiarism_score function
    """

    def test_calculate_text_plagiarism_score_ideal(self):
        """
        Tests that calculate_text_plagiarism_score function
            can handle simple ideal input case
        """
        original_text_tokens = (('the', 'cat', 'appeared'),
                                ('the', 'dog', 'disappeared'))
        suspicious_text_tokens = (('the', 'man', 'arrived'),
                                  ('the', 'boy', 'left'))
        plagiarism_threshold = 0.3

        expected = (1/3+1/3)/2
        actual = calculate_text_plagiarism_score(original_text_tokens,
                                                 suspicious_text_tokens,
                                                 plagiarism_threshold)
        self.assertEqual(expected, actual)

    def test_calculate_text_plagiarism_score_max(self):
        """
        Tests that calculate_text_plagiarism_score function
            can generate max plagiarism correctly
        """
        sentence = (('the', 'cat', 'left'),
                    ('the', 'dog', 'disappeared'))
        plagiarism_threshold = 0.3

        expected = ((3/3+3/3)/2)
        actual = calculate_text_plagiarism_score(sentence, sentence, plagiarism_threshold)
        self.assertEqual(expected, actual)

    def test_calculate_text_plagiarism_score_min(self):
        """
        Tests that calculate_text_plagiarism_score function
            can generate min plagiarism correctly
        """
        text = (('the', 'cat', 'left'),
                ('the', 'dog', 'disappeared'))
        suspicious_text_tokens = (('a', 'man', 'arrived'),
                                  ('a', 'boy', 'left'))
        plagiarism_threshold = 0.3

        expected = 0.0
        actual = calculate_text_plagiarism_score(text, suspicious_text_tokens, plagiarism_threshold)
        self.assertEqual(expected, actual)

    def test_calculate_text_plagiarism_score_incorrect_text_input(self):
        """
        Tests that calculate_text_plagiarism_score function
            can handle incorrect texts inputs
        """
        text_patches = (('the', 'cat', 'left'),
                        ('the', 'dog', 'disappeared'))
        plagiarism_threshold = 0.3

        bad_inputs = [[], {}, ((None,),), 9.22, -1, 0, -6, None, True, (('',), None)]
        expected = -1
        for bad_input in bad_inputs:
            actual = calculate_text_plagiarism_score(text_patches,
                                                     bad_input,
                                                     plagiarism_threshold)
            actual_second = calculate_text_plagiarism_score(bad_input,
                                                            text_patches,
                                                            plagiarism_threshold)
            self.assertEqual(expected, actual)
            self.assertEqual(expected, actual_second)

    def test_calculate_text_plagiarism_score_empty_texts(self):
        """
        Tests that calculate_text_plagiarism_score function
            can handle empty texts inputs
        """
        empty_text = ((), ())
        patches_texts = (('the', 'cat', 'left'),
                         ('the', 'dog', 'disappeared'))
        plagiarism_threshold = 0.3

        expected = 0.0
        actual = calculate_text_plagiarism_score(empty_text, patches_texts, plagiarism_threshold)
        actual_second = calculate_text_plagiarism_score(patches_texts, empty_text, plagiarism_threshold)
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_second)

    def test_calculate_text_plagiarism_score_check_output(self):
        """
        Tests that calculate_text_plagiarism_score function
            can generate correct output according to given specs
        """
        original_text_tokens = (('the', 'cat', 'appeared'),
                                ('the', 'dog', 'disappeared'))
        suspicious_text_tokens = (('the', 'man', 'arrived'),
                                  ('the', 'boy', 'left'))
        plagiarism_threshold = 0.3

        expected = float
        actual = type(calculate_text_plagiarism_score(original_text_tokens,
                                                      suspicious_text_tokens,
                                                      plagiarism_threshold))
        self.assertTrue(expected, actual)

    def test_calculate_text_plagiarism_score_incorrect_threshold(self):
        """
        Tests that calculate_text_plagiarism_score function
            can handle incorrect threshold input
        """
        patches_texts = (('the', 'cat', 'left'),
                         ('the', 'dog', 'disappeared'))
        bad_inputs = [[], {}, '', -1, -6.34, -6, 1.2, None, True, (None, None)]

        expected = -1
        for bad_input in bad_inputs:
            actual = calculate_text_plagiarism_score(patches_texts,
                                                     patches_texts,
                                                     bad_input)
            self.assertEqual(expected, actual)

    def test_calculate_text_plagiarism_score_reversed_behaviour(self):
        """
        Tests that calculate_text_plagiarism_score function
            can generate correct behaviour if replace texts with each other
        """
        original_text_tokens = (('the', 'cat', 'appeared'),
                                ('the', 'dog', 'disappeared'))
        suspicious_text_tokens = (('the', 'man', 'arrived'),
                                  ('the', 'boy', 'left'))
        plagiarism_threshold = 0.1

        expected = (1/3+1/3)/2
        actual = calculate_text_plagiarism_score(original_text_tokens,
                                                 suspicious_text_tokens,
                                                 plagiarism_threshold)
<<<<<<< HEAD
        actual_reversed = calculate_text_plagiarism_score(original_text_tokens,
                                                          suspicious_text_tokens,
                                                          plagiarism_threshold)
=======
        actual_reversed = calculate_text_plagiarism_score(suspicious_text_tokens,
                                                          original_text_tokens,
                                                          plagiarism_threshold=0.1)
>>>>>>> cd2909df66a6e74a9c6263dfcf079164a12bfdd3
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_reversed)

    def test_calculate_text_plagiarism_score_bigger_first_text(self):
        """
        Tests that calculate_text_plagiarism_score function
            can handle different first text lengths inputs
        """
        original_text_tokens = (('the', 'cat', 'appeared'),
                                ('the', 'dog', 'disappeared'),
                                (),
                                ())
        suspicious_text_tokens = (('the', 'girl', 'arrived'),
                                  ('the', 'boy', 'left'))
        plagiarism_threshold = 0.1

        expected = (1/3+1/3)/2
        actual = calculate_text_plagiarism_score(original_text_tokens,
                                                 suspicious_text_tokens,
                                                 plagiarism_threshold)
        self.assertEqual(expected, actual)

    def test_calculate_text_plagiarism_score_bigger_first_text_complex(self):
        """
        Tests that calculate_text_plagiarism_score function
            can handle different first text lengths complex inputs
        """
        original_text_tokens = (('the', 'cat', 'appeared'),
                                ('the', 'dog', 'disappeared'),
                                (),
                                ())
        suspicious_text_tokens = ((),
                                  ('the', 'girl', 'arrived'),
                                  ('the', 'boy', 'left'))
        plagiarism_threshold = 0.3

        expected = (0+1/3+0)/3
        actual = calculate_text_plagiarism_score(original_text_tokens,
                                                 suspicious_text_tokens,
                                                 plagiarism_threshold)
        self.assertEqual(expected, actual)

    def test_calculate_text_plagiarism_score_bigger_second_text(self):
        """
        Tests that calculate_text_plagiarism_score function
            can handle bigger second texts inputs
        """
        original_text_tokens = ((),
                                ('the', 'girl', 'arrived'),
                                ('the', 'boy', 'left'))
        suspicious_text_tokens = (('the', 'cat', 'appeared'),
                                  ('the', 'dog', 'disappeared'),
                                  (),
                                  ())
        plagiarism_threshold = 0.3
        expected = (0+1/3+0+0)/4

        actual = calculate_text_plagiarism_score(original_text_tokens,
                                                 suspicious_text_tokens,
                                                 plagiarism_threshold)
        self.assertEqual(expected, actual)

    def test_calculate_text_plagiarism_score_check_threshold(self):
        """
        Tests that calculate_text_plagiarism_score function
            can preprocess given threshold correctly
        """
        original_text_tokens = (('the', 'cat', 'appeared'),
                                ('the', 'dog', 'disappeared'),
                                (),
                                ())
        suspicious_text_tokens = ((),
                                  ('the', 'girl', 'arrived'),
                                  ('the', 'boy', 'left'))
        plagiarism_threshold = 0.3

        expected = (0+1/3+0)/3
        actual = calculate_text_plagiarism_score(original_text_tokens,
                                                 suspicious_text_tokens,
                                                 plagiarism_threshold)
        self.assertEqual(expected, actual)

    @patch('lab_2.main.calculate_plagiarism_score', side_effect=calculate_plagiarism_score)
    def test_calculate_text_plagiarism_score_calls_required_function(self, mock):
        """
        Tests that calculate_text_plagiarism_score function
            calls calculate_plagiarism_score function
        """
        patches_texts = (('the', 'cat', 'left'),
                         ('the', 'dog', 'disappeared'))

        calculate_text_plagiarism_score(patches_texts,
                                        patches_texts,
                                        plagiarism_threshold=0.3)
        self.assertTrue(mock.called)


if __name__ == "__main__":
    unittest.main()
