"""
Longest common subsequence implementation starter
"""
import main


if __name__ == '__main__':
    origin = main.tokenize_big_file('lab_2/data.txt')[:10000]
    print(f"Original text length is {len(origin)} tokens.")

    suspicious = main.tokenize_big_file('lab_2/data_2.txt')[:10000]
    print(f"Suspicious text length is {len(suspicious)} tokens.")

    lcs_length = main.find_lcs_length_optimized(origin, suspicious, plagiarism_threshold=0.3)
    print(f"Longest common subsequence consists of {lcs_length} word(s).")

    actual = main.calculate_plagiarism_score(lcs_length, suspicious)
    print(f"Plagiarism score: {actual:.1f}%")

    RESULT = actual
    EXPECTED = 0.0

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == EXPECTED, 'Concordance not working'
