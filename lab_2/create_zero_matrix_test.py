"""
Tests create_zero_matrix function
"""

import unittest
from lab_2.main import create_zero_matrix


class ZeroMatrixTest(unittest.TestCase):
    """
    Checks for create_zero_matrix function
    """

    def test_create_zero_matrix_ideal(self):
        """
        Tests that create_zero_matrix function
            can handle simple input
        """
        expected = [[0, 0], [0, 0]]
        actual = create_zero_matrix(2, 2)
        self.assertEqual(expected, actual)

    def test_create_zero_matrix_3_3(self):
        """
        Tests that create_zero_matrix function
            can handle 3_3 matrix
        """
        expected = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        actual = create_zero_matrix(3, 3)
        self.assertEqual(expected, actual)

    def test_create_zero_matrix_complex(self):
        """
        Tests that create_zero_matrix function
            can handle different rows and columns
        """
        expected = [[0, 0, 0, 0], [0, 0, 0, 0]]
        actual = create_zero_matrix(2, 4)
        self.assertEqual(expected, actual)

    def test_create_zero_matrix_bad_inputs(self):
        """
        Tests that create_zero_matrix function
            can handle bad inputs
        """
        expected = []
        bad_inputs = [[], {}, (), '', 9.22, -1, 0, -6, None, True]
        for bad_input in bad_inputs:
            actual_left = create_zero_matrix(bad_input, 1)
            actual_right = create_zero_matrix(1, bad_input)
            self.assertEqual(expected, actual_left)
            self.assertEqual(expected, actual_right)

    @unittest.skip
    def test_create_zero_matrix_stress_test(self):
        """
        Tests that create_zero_matrix function
            can raise error in case of unexpected calculations
        """
        self.assertRaises(RuntimeError, create_zero_matrix, 1000000, 1000000)

    def test_create_zero_matrix_output_check(self):
        """
        Tests that create_zero_matrix function
            can generate correct output according to given specs
        """
        all_zeroes = True
        actual = create_zero_matrix(2, 2)
        for row in actual:
            for column in row:
                if column != 0:
                    all_zeroes = False
                    break
        self.assertTrue(all_zeroes)
