"""
Longest common subsequence implementation starter
"""


from lab_2.main import tokenize_by_lines, accumulate_diff_stats, create_diff_report


if __name__ == '__main__':
    # my texts here
    ORIGINAL_TEXT = """
    Stephanie recently took a weekend trip to Los Angeles, California. 
    Los Angeles is a coastal city situated along the Pacific Ocean. 
    Many celebrities earned their claim to fame here. 
    Although the town offers many attractions centered around Hollywood culture, 
    there is a lot to see and visit in Los Angeles.
    """
    SUSPICIOUS_TEXT = """
    Kitty recently took the weekend trip to Los Angeles, California. 
    Los Angeles is a big city situated along the Pacific Ocean. 
    Many celebrities earned their right to fame here. 
    Although the city offers many attractions centered around Hollywood culture, 
    there is a lot to see and visit in Los Angeles.
    """

    #  here goes your logic: calling methods from concordance.py
    original_tokens = tokenize_by_lines(ORIGINAL_TEXT)
    suspicious_tokens = tokenize_by_lines(SUSPICIOUS_TEXT)
    stats = accumulate_diff_stats(original_tokens, suspicious_tokens)
    report = create_diff_report(original_tokens, suspicious_tokens, stats)

    RESULT = stats['sentence_lcs_length']
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [8, 10, 7, 20]
