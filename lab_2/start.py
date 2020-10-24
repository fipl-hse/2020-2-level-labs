"""
Longest common subsequence implementation starter
"""
from lab_2 import main
if __name__ == "__main__":
    original_text = '''
    Once upon a time a little cat Meow walked down the street.
    She met her friend, a giant dog Bow.
    And they continued their walk together.
    '''
    suspicious_text = '''
    Once upon a time a giant dog Bow walked down the street.
    He met his friend, a little cat Meow.
    And they went to the theatre.
    '''

    plagiarism_threshold = 0.3
    tuple_original = main.tokenize_by_lines(original_text)
    tuple_suspicious = main.tokenize_by_lines(suspicious_text)
    lcs_matrix = main.fill_lcs_matrix(tuple_original,tuple_suspicious)
    max_length = main.find_lcs_length(tuple_original, tuple_suspicious, plagiarism_threshold)
    LCS = main.find_lcs(tuple_original,tuple_suspicious,lcs_matrix)
    plagiarism = main.calculate_plagiarism_score(max_length,tuple_suspicious)
    calculate_plagiarism = main.calculate_plagiarism_score(tuple_original,tuple_suspicious)
    texts_plagiarism = main.calculate_text_plagiarism_score(tuple_original,tuple_suspicious,plagiarism_threshold)

    RESULT = texts_plagiarism
    assert RESULT == 0.4861111111111111, "Checking not working"

