"""
Tests find_diff_in_sentence function
"""

import unittest
from lab_2.main import find_diff_in_sentence


class FindDiffInSentence(unittest.TestCase):
    """
    Checks for find_diff_in_sentence function
    """

    def test_find_diff_in_sentence_ideal(self):
        """
        Tests that find_diff_in_sentence function
            can handle ideal simple input
        """
        first_sentence = ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur')
        second_sentence = ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur')
        lcs = ('its', 'body', 'is', 'covered', 'with', 'fur')

        expected = ((5, 7), (5, 7))
        actual = find_diff_in_sentence(first_sentence, second_sentence, lcs)
        self.assertEqual(expected, actual)

    def test_find_diff_in_sentence_end_sentence_diff(self):
        """
        Tests that find_diff_in_sentence function
            can handle correct diff in the end of sentences
        """
        first_sentence = ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white')
        second_sentence = ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black')
        lcs = ('its', 'body', 'is', 'covered', 'with')

        expected = ((5, 7), (5, 7))
        actual = find_diff_in_sentence(first_sentence, second_sentence, lcs)
        self.assertEqual(expected, actual)

    def test_find_diff_in_sentence_start_sentence_diff(self):
        """
        Tests that find_diff_in_sentence function
            can handle correct diff in the start of sentence
        """
        first_sentence = ('his', 'body', 'is', 'covered', 'with', 'bushy', 'white')
        second_sentence = ('her', 'body', 'is', 'covered', 'with', 'bushy', 'white')
        lcs = ('body', 'is', 'covered', 'with', 'bushy', 'white')

        expected = ((0, 1), (0, 1))
        actual = find_diff_in_sentence(first_sentence, second_sentence, lcs)
        self.assertEqual(expected, actual)

    def test_find_diff_in_sentence_no_diff(self):
        """
        Tests that find_diff_in_sentence function can handle maximum same sentences
        """
        first_sentence = ('his', 'body', 'is', 'covered', 'with', 'bushy', 'white')

        expected = ((), ())
        actual = find_diff_in_sentence(first_sentence, first_sentence, first_sentence)
        self.assertEqual(expected, actual)

    def test_find_diff_in_sentence_diff(self):
        """
        Tests that find_diff_in_sentence function
            can handle sentences with max diff
        """
        first_sentence = ('the', 'cat', 'left')
        second_sentence = ('a', 'dog', 'appeared')
        lcs = ()

        expected = ((0, 3), (0, 3))
        actual = find_diff_in_sentence(first_sentence, second_sentence, lcs)
        self.assertEqual(expected, actual)

    def test_find_diff_in_sentence_incorrect_inputs(self):
        """
        Tests that find_diff_in_sentence function
            can handle incorrect inputs
        """
        patches_sentence = ('the', 'cat', 'left')
        bad_inputs = [[], {}, '', 9.22, -1, 0, -6, None, True, (None,)]

        expected = ()
        for bad_input in bad_inputs:
            actual_first_sentence = find_diff_in_sentence(bad_input,
                                                          patches_sentence,
                                                          patches_sentence)
            actual_second_sentence = find_diff_in_sentence(patches_sentence,
                                                           bad_input,
                                                           patches_sentence)
            actual_lcs_sentence = find_diff_in_sentence(patches_sentence,
                                                        patches_sentence,
                                                        bad_input)
            self.assertEqual(expected, actual_first_sentence)
            self.assertEqual(expected, actual_second_sentence)
            self.assertEqual(expected, actual_lcs_sentence)

    def test_find_diff_in_sentence_check_output(self):
        """
        Tests that find_diff_in_sentence function
            can generate correct output according to given specs
        """
        sentence_first = ('the', 'cat', 'disappeared')
        sentence_second = ('the', 'dog', 'disappeared')
        lcs = ('the', 'disappeared')

        expected = tuple
        actual = type(find_diff_in_sentence(sentence_first, sentence_second, lcs))
        self.assertEqual(expected, actual)

    def test_find_diff_in_sentence_reverse_behaviour(self):
        """
        Tests that find_diff_in_sentence function
            can change same sentences without changing answer
        """
        first_sentence = ('its', 'body', 'is', 'covered', 'with', 'bushy')
        second_sentence = ('its', 'body', 'is', 'covered', 'with', 'shiny')
        lcs = ('its', 'body', 'is', 'covered', 'with')

        expected = ((5, 6), (5, 6))
        actual = find_diff_in_sentence(first_sentence, second_sentence, lcs)
        actual_reversed = find_diff_in_sentence(second_sentence, first_sentence, lcs)
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_reversed)

    def test_find_diff_in_sentence_empty_sentence(self):
        """
        Tests that find_diff_in_sentence function can handle empty sentence inputs
        """
        first_sentence = ()
        second_sentence = ('a', 'dog', 'appeared')
        lcs = ()

        expected = ((), ())
        actual = find_diff_in_sentence(first_sentence, second_sentence, lcs)
        self.assertEqual(expected, actual)

    def test_find_diff_in_sentence_many(self):
        """
        Tests that find_diff_in_sentence function
            can handle several diffs
        """
        first_sentence = ('his', 'body', 'is', 'covered', 'with', 'bushy', 'white')
        second_sentence = ('her', 'body', 'is', 'covered', 'with', 'shiny', 'black')
        lcs = ('body', 'is', 'covered', 'with')

        expected = ((0, 1, 5, 7), (0, 1, 5, 7))
        actual = find_diff_in_sentence(first_sentence, second_sentence, lcs)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
