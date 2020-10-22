"""
Longest common subsequence implementation starter
"""
import main

original_text_tokens = (('I', 'want', 'a', 'dog'),
                                ('it', 'is', 'a', 'doberman', 'with', 'smooth', 'brown', 'fur'))
suspicious_text_tokens = (('I', 'want', 'a', 'dog'),
                                  ('it', 'is', 'a', 'dachshund', 'with', 'smooth', 'black', 'fur'))

accumulated_diff_stats = main.accumulate_diff_stats(original_text_tokens, suspicious_text_tokens)
actual = main.create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats).split()
RESULT = main.create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats).split()

assert RESULT == ['-', 'I', 'want', 'a', 'dog', '+', 'I, 'want', 'a', 'dog', 'lcs', '=', '4,', 'plagiarism',
           '=', '100.0%', '-', 'it', 'is', 'a', '|','doberman', '|','with',  'smooth', '|','brown', '|', 'fur',
           '+', 'it', 'is', 'a', '|','dachshund', '|', 'with', 'smooth', '|', 'black', '|', 'fur', 'lcs', '=',
           '6,', 'plagiarism', '=', '75.0%', 'Text', 'average', 'plagiarism', '(words):', '87.5%'], 'diff_report ' \
                                                                                                    'not working'

