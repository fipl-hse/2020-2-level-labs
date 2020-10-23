"""
Longest common subsequence implementation starter
"""
import lab_2.main


if __name__ == '__main__':
    sentence_tokens_first_text = lab_2.main.tokenize_big_file('lab_2/data.txt')[:20000]
    sentence_tokens_second_text = lab_2.main.tokenize_big_file('lab_2/data_2.txt')[:20000]
    PLAGIARISM = 0.0001
    lcs_length = lab_2.main.find_lcs_length_optimized(sentence_tokens_first_text,
                                                      sentence_tokens_second_text,
                                                      PLAGIARISM)
    actual = lcs_length / len(sentence_tokens_second_text)
    EXPECTED = 2580 / 20000
    RESULT = actual
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == EXPECTED, 'Results differ'
