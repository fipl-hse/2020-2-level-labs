"""
Longest common subsequence implementation starter
"""


import main

def text_plagiarism_score_for_big_files():
    sentence_tokens_first_text = main.tokenize_big_file('data.txt')
    sentence_tokens_second_text = main.tokenize_big_file('data_2.txt')
    plagiarism_threshold = 0.0001

    lcs_length = main.find_lcs_length_optimized(sentence_tokens_first_text,
                                                sentence_tokens_second_text,
                                                plagiarism_threshold)
    score = lcs_length / len(sentence_tokens_second_text)

    print(f'The text plagiarism score for big files: {score:.2f}\n\n')
    return score


#if __name__ == '__main__':
#    RESULT = text_plagiarism_score_for_big_files()
#    assert RESULT, 'Plagiarism checker not working'
