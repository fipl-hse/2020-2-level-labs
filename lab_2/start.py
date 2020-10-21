"""
Longest common subsequence implementation starter
"""
import main
if __name__ == '__main__':
    original_text_tokens = (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'fun'), ('he', 'is', 'sleeping'))
    suspicious_text_tokens = (('i', 'have', 'a', 'dog'), ('his', 'name', 'is', 'hugo'), ('he', 'is', 'running'))
    accumulated_diff_stats = main.accumulate_diff_stats(original_text_tokens, suspicious_text_tokens)
    res = main.create_diff_report(original_text_tokens, suspicious_text_tokens,accumulated_diff_stats)
    RESULT = res.split('\n')
    assert RESULT == ['- i have a | cat |', '+ i have a | dog |', '', 'lcs = 3, plagiarism = 75.0%', '',
                      '- his name is | fun |', '+ his name is | hugo |', '', 'lcs = 3, plagiarism = 75.0%', '',
                      '- he is | sleeping |', '+ he is | running |', '', 'lcs = 2, plagiarism = 66.66666666666666%', '',
                      'Text average plagiarism (words): 72.22222222222221%']
