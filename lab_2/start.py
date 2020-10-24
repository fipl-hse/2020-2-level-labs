from lab_2 import main
if __name__ == "__main__":
    original_text_tokens =  (('there', 'is', 'a', 'story', 'people', 'need', 'to', 'know'),
                            ('when', 'you', 'find', 'the', 'one', 'never', 'let', 'them', 'go'),
                            ('if', 'it', 'feels', 'just', 'right', 'let', 'it', 'be', 'the', 'same'),
                            ('if', 'you', 'found', 'the', 'one', 'means', 'you', 'found', 'your', 'way'))

    suspicious_text_tokens = (('look', 'theres', 'something', 'i', 'want', 'you', 'to', 'know'),
                             ('when', 'you', 'mess', 'up', 'sometimes', 'never', 'give', 'up', 'k'),
                             ('if', 'it', 'feels', 'wrong', 'never', 'let', 'it', 'be', 'the', 'same'),
                             ('keep', 'fighting', 'cos', 'all', 'you', 'need', 'is', 'to', 'your', 'way'))

    plagiarism_threshold = 0.3

    lcs_matrix = main.fill_lcs_matrix(original_text_tokens, suspicious_text_tokens)
    lcs_length = main.find_lcs_length(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)
    lcs = main.find_lcs(original_text_tokens, suspicious_text_tokens, lcs_matrix)
    plag_score = main.calculate_plagiarism_score(lcs_length, suspicious_text_tokens)
    calculate_plag_score = main.calculate_plagiarism_score(original_text_tokens, suspicious_text_tokens)
    text_plag_score = main.calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)

    RESULT = text_plag_score
    assert RESULT == 0.35833333333333334, 'Checking not working'