"""
Longest common subsequence implementation starter
"""
<<<<<<< Updated upstream
import lab_2.main

if __name__ == '__main__':
    original_text_tokens = (('i', 'have', 'a', 'cat'),
                            ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur'))
    suspicious_text_tokens = (('i', 'have', 'a', 'cat'),
                              ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur'))
    accumulated_diff_stats = lab_2.main.accumulate_diff_stats(original_text_tokens, suspicious_text_tokens)

    expected = open('lab_2/diff_report_example.txt', 'r', errors='coerce').read().split()
    actual = lab_2.main.create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats).split()

    RESULT = actual
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == expected, 'Results differ'
=======
import main

ORIGINAL_TEXT = 'the cat is sleeping'
SUSPICIOUS_TEXT = 'the little cat is running'

original_tokens = main.tokenize_by_lines(ORIGINAL_TEXT)
suspicious_tokens = main.tokenize_by_lines(SUSPICIOUS_TEXT)

print("Tokenized original text:", original_tokens)
print("Tokenized suspicious text:", suspicious_tokens)

lcs_length = main.find_lcs_length(original_tokens, suspicious_tokens, plagiarism_threshold=0.3)
print("Length of the longest common subsequence:", lcs_length)

matrix = main.fill_lcs_matrix(original_tokens, suspicious_tokens)

lcs = main.find_lcs(original_tokens, suspicious_tokens, matrix)
print("The longest common subsequence:", lcs)

plagiarism_score = main.calculate_plagiarism_score(lcs_length, suspicious_tokens)
print("The plagiarism score:", plagiarism_score)

text_plagiarism_score = main.calculate_text_plagiarism_score(original_tokens, suspicious_tokens, plagiarism_score)
print("Text average plagiarism:", text_plagiarism_score)

RESULT = text_plagiarism_score
assert RESULT, 'Not working'
>>>>>>> Stashed changes
