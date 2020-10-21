"""
Longest common subsequence implementation starter
"""
import main


if __name__ == '__main__':
    origin = main.tokenize_big_file('data.txt')
    suspicious = main.tokenize_big_file('data_2.txt')

    # I've changed `find_lcs_length` function to the optimized version in the `calculate_text_plagiarism_score`
    # function to demonstrate usage of the optimized function from the step #11

    actual = main.calculate_text_plagiarism_score(origin, suspicious)
    RESULT = actual

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

