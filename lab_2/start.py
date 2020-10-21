"""
Longest common subsequence implementation starter
"""

import main

original_text_tokens = (('i', 'have', 'a', 'cat'),
                                ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur'))
suspicious_text_tokens = (('i', 'have', 'a', 'cat'),
                                  ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur'))

accumulated_diff_stats = main.accumulate_diff_stats(original_text_tokens, suspicious_text_tokens)
actual = main.create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats).split()
RESULT = main.create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats).split()

assert RESULT
