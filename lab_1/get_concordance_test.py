# pylint: skip-file
"""
Checks the first lab concordance building function
"""

import unittest
from main import get_concordance
from main import tokenize
from main import read_from_file


class GetConcordanceTest(unittest.TestCase):
    """
    Tests get concordance function
    """

    def test_get_concordance_ideal(self):
        """
        Ideal get concordance scenario
        """
        expected = [['man', 'is', 'happy', 'the', 'dog', 'is']]
        actual = get_concordance(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                                  'the', 'dog', 'is', 'glad', 'but', 'the', 'cat', 'is', 'sad'],
                                 'happy', 2, 3)
        self.assertEqual(expected, actual)

    def test_get_concordance_several_contexts(self):
        """
        Checks that a concordance list can be created for several contexts
        """
        expected = [['man', 'is', 'happy', 'the', 'dog', 'is'], ['dog', 'is', 'happy', 'but', 'the', 'cat']]
        actual = get_concordance(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                                  'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad'],
                                 'happy', 2, 3)
        self.assertEqual(expected, actual)

    def test_get_concordance_empty_inputs(self):
        """
        Checks that function can handle empty argument inputs
        """
        expected = []
        actual = get_concordance([], 'happy', 2, 3)
        self.assertEqual(expected, actual)
        actual = get_concordance(['happy'], '', 2, 3)
        self.assertEqual(expected, actual)
        expected = []
        actual = get_concordance(['happy'], 'happy', 0, 0)
        self.assertEqual(expected, actual)

    def test_get_concordance_bad_number_inputs(self):
        """
        Checks that function can handle incorrect number inputs
        """
        expected = []
        actual = get_concordance(['happy', 'man'], 'happy', -1, 0)
        self.assertEqual(expected, actual)
        expected = [['happy', 'man']]
        actual = get_concordance(['happy', 'man'], 'happy', 0, 1)
        self.assertEqual(expected, actual)
        expected = []
        actual = get_concordance(['happy', 'man'], 'man', -1, 0)
        self.assertEqual(expected, actual)

    def test_get_concordance_big_right_number_input(self):
        """
        Checks if function can handle great right range numbers,
        that exceed the number of given tokens
        """
        expected = [['happy', 'man']]
        actual = get_concordance(['one', 'happy', 'man'], 'happy', 0, 1000)
        self.assertEqual(expected, actual)

    def test_get_concordance_big_left_number_input(self):
        """
        Checks if function can handle great left range numbers,
        that exceed the number of given tokens
        """
        expected = [['one', 'happy']]
        actual = get_concordance(['one', 'happy', 'man'], 'happy', 1000, 0)
        self.assertEqual(expected, actual)

    def test_get_concordance_bad_inputs(self):
        """
        Checks that function can handle incorrect inputs
        """
        bad_inputs = [[], {}, 'string', (), None, 9.34, True, [None]]
        expected = []
        for bad_input in bad_inputs:
            actual_1 = get_concordance(['happy', 'man', 'went'], 'man', bad_input, bad_input)
            actual_2 = get_concordance(bad_input, 'happy', 2, 3)
            actual_3 = get_concordance(['happy', 'man', 'went'], bad_input, 1, 2)
            self.assertEqual(expected, actual_1)
            self.assertEqual(expected, actual_2)
            self.assertEqual(expected, actual_3)

    def test_big_text_get_concordance_term(self):
        """
        Checks if a context for a given term can be found properly
        """
        text = read_from_file('lab_1/data.txt')
        tokens = tokenize(text)

        expected = [['although', 'less', 'compact', 'than', 'tex', 'the',
                     'xml', 'structuring', 'promises', 'to', 'make', 'it',
                     'widely', 'usable', 'and', 'allows', 'for', 'instant',
                     'display', 'in', 'applications', 'such', 'as', 'web',
                     'browsers', 'and', 'facilitates', 'an', 'interpretation',
                     'of', 'its', 'meaning', 'in', 'mathematical', 'software', 'products']]
        actual = get_concordance(tokens, 'tex', 4, 31)
        self.assertEqual(expected, actual)

    def test_get_concordance_several_contexts_big_text(self):
        """
        Checks if contexts for a given term can be found in real text properly
        """
        text = read_from_file('lab_1/data.txt')
        tokens = tokenize(text)

        expected = [['epithelial', 'sodium', 'channels'],
                    ['means', 'sodium', 'aluminate'],
                    ['by', 'sodium', 'bicarbonate'],
                    ['the', 'sodium', 'salt']]
        actual = get_concordance(tokens, 'sodium', 1, 1)
        self.assertEqual(expected, actual)
