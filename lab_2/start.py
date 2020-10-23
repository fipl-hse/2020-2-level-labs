"""
Longest common subsequence implementation starter
"""
import main

if __name__ == '__main__':

    TOKENIZED = 'I have a cat.\nHis name is Bruno'
    print(f"Tokenized by lines:\n>> {TOKENIZED} <<\n")

    origin = ('the', 'dog', 'sleeps')
    suspicious = ('the', 'cat', 'is', 'sleeping')

    lcs_matrix = main.fill_lcs_matrix(origin, suspicious)
    print('LCS matrix: \n')

    for row in lcs_matrix:
        print(row)
    print()

    lcs_length = main.find_lcs_length(origin, suspicious, plagiarism_threshold=0.3)
    print(f"LCS length is {lcs_length} word(s).\n")

    lcs_length = main.find_lcs_length_optimized(origin, suspicious, plagiarism_threshold=0.3)
    print(f"Longest common subsequence (optimized) consists of {lcs_length} word(s).\n")

    actual = main.calculate_plagiarism_score(lcs_length, suspicious)
    print(f"Plagiarism score: {actual:.1f}%\n")

    lcs = main.find_lcs(origin, suspicious, lcs_matrix)
    print(f"LCS is >> {lcs} <<\n")

    diffs = main.find_diff_in_sentence(origin, suspicious, lcs)
    print(f"Differences >> {diffs} <<\n")

    plagiarism_score = main.calculate_plagiarism_score(lcs_length, suspicious)
    print(f"Plagiarism score is {plagiarism_score:.1f}%\n")

    origin = (('the', 'cat', 'appeared'),
              ('the', 'dog', 'disappeared'))
    suspicious = (('the', 'man', 'arrived'),
                  ('the', 'boy', 'left'))

    text_plagiarism_score = main.calculate_text_plagiarism_score(origin, suspicious)
    print(f"Text plagiarism score is {text_plagiarism_score:.1f}%\n")

    accumulated_diff_stats = main.accumulate_diff_stats(origin, suspicious)

    for param in accumulated_diff_stats.items():
        print(f"{param[0]}: {param[1]}")
    print()

    DIFF_REPORT = main.create_diff_report(origin, suspicious, accumulated_diff_stats)
    print(DIFF_REPORT)

    RESULT = accumulated_diff_stats
    EXPECTED = {
        'text_plagiarism': 0.3333333333333333,
        'sentence_plagiarism': [0.3333333333333333, 0.3333333333333333],
        'sentence_lcs_length': [1, 1],
        'difference_indexes': [((1, 3), (1, 3)), ((1, 3), (1, 3))]
    }

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == EXPECTED, 'Concordance not working'
