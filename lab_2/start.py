"""
Longest common subsequence implementation starter
"""
import main


if __name__ == '__main__':
    original_tokens = main.tokenize_big_file('lab_2/data.txt'[:3000])
    suspicious_tokens = main.tokenize_big_file('lab_2/data_2.txt'[:3000])
    lcs_length = main.find_lcs_length_optimized(original_tokens, suspicious_tokens, 0.0001)
    print('Longest common subsequence consists of {} words.'.format(lcs_length))
    actual = main.calculate_plagiarism_score(lcs_length, suspicious_tokens)
    print('The ratio of borrowings from the first text in the second text is {}'.format(actual))
    RESULT = 60 / 502

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Calculation of text plagiarism is not working'
