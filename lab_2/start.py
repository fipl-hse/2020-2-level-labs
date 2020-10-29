
"""
Longest common subsequence implementation starter
"""
import main


original_text_tokens = (('i', 'have', 'a', 'cat'),
                                ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur'))
suspicious_text_tokens = (('i', 'have', 'a', 'cat'),
                                  ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur'))

RESULT = main.create_diff_report
assert RESULT