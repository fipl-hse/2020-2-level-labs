"""
Longest common subsequence implementation starter
"""
import main

if __name__ == '__main__':
    original_tokens = main.tokenize_big_file('lab_2/data.txt')
    suspicious_tokens = main.tokenize_big_file('lab_2/data_2.txt')
    RESULT = main.calculate_text_plagiarism_score(original_tokens, suspicious_tokens)
