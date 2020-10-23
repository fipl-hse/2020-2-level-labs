"""
Longest common subsequence implementation starter
"""

import main
from tokenizer import tokenize


def test_till_calculate_plagiarism_score():
    origin_text = 'the big cat is sleeping'
    susp_text = 'the cat is big'

    origin_tokens = tokenize(origin_text)
    susp_tokens = tokenize(susp_text)

    print(f'Raw text: {origin_text}')
    print(f'Tokenized text: {origin_tokens}\n\n')

    lcs_lenght = main.find_lcs_length(origin_tokens,
                                      susp_tokens,
                                      plagiarism_threshold=0.0)
    print('A length of the longest common subsequence for \n\n'
        f'{origin_text} \n\nand \n\n{susp_text}: \n\n{lcs_lenght} \n')

    matrix = main.fill_lcs_matrix(origin_tokens, susp_tokens)
    print('A matrix:')
    print(*matrix, sep='\n', end='\n\n')

    longest_lcs = main.find_lcs(origin_tokens, susp_tokens, matrix)
    print(f'The longest common subsequence: {longest_lcs}')

    score = main.calculate_plagiarism_score(lcs_lenght, susp_tokens)
    print(f'The plagiarism score: {score:.2f}\n')
    return score

def test_calculate_text_plagiarism_score():
    origin_text = '''the cat is big
the sun is beatiful
the moon is rising'''

    susp_text = '''the big cat
the beatiful sun was rising 
a blue moon will rise'''

    origin_tokens = main.tokenize_by_lines(origin_text)
    susp_tokens = main.tokenize_by_lines(susp_text)

    score = main.calculate_text_plagiarism_score(origin_tokens,
                                                 susp_tokens)

    print('The text plagiarism score for \n\n'
        f'{origin_text} \n\n and \n\n{susp_text}: \n\n{score:.2f}\n\n')
    return score

def test_find_diff():
    origin_text = 'a big cat loves a small cat'
    susp_text = 'a dog loves a cat'

    origin_tokens = tokenize(origin_text)
    susp_tokens = tokenize(susp_text)

    matrix = main.fill_lcs_matrix(origin_tokens, susp_tokens)

    lcs = main.find_lcs(origin_tokens, susp_tokens, matrix)

    difference = main.find_diff_in_sentence(origin_tokens, susp_tokens, lcs)

    print('The difference indexes between \n\n'
        f'{origin_text} \n\n and \n\n{susp_text}: \n\n{difference})
    return difference

def test_accumulated_stat_and_report():
    origin_text = '''the cat is big
the sun is beatiful
the moon is rising'''

    susp_text = '''the cat is big
the beatiful sun was rising 
a blue moon will rise'''

    origin_tokens = main.tokenize_by_lines(origin_text)
    susp_tokens = main.tokenize_by_lines(susp_text)

    stat = main.accumulate_diff_stats(origin_tokens, susp_tokens)

    print('The accumulated main statistics for pairs of sentences in texts: \n\n'
        f'{origin_text} \n\n and \n\n{susp_text}: \n')
    print(*stat.items(), sep='\n', end='\n\n')

    report = main.create_diff_report(origin_tokens,
                                     susp_tokens,
                                     stat)
    print(f'A report:\n\n{report}\n')
    return report

def text_plagiarism_score_for_big_files():
    sentence_tokens_first_text = main.tokenize_big_file('lab_2/data.txt')
    sentence_tokens_second_text = main.tokenize_big_file('lab_2/data_2.txt')
    plagiarism_threshold = 0.0001

    lcs_length = main.find_lcs_length_optimized(sentence_tokens_first_text,
                                                sentence_tokens_second_text,
                                                plagiarism_threshold)
    score = lcs_length / len(sentence_tokens_second_text)

    print(f'The text plagiarism score for big files: {score:.2f}\n\n')
    return score


if __name__ == '__main__':
    #RESULT = test_till_calculate_plagiarism_score()
    #RESULT = test_calculate_text_plagiarism_score()
    #RESULT = test_find_diff()
    RESULT = test_accumulated_stat_and_report()
    #RESULT = text_plagiarism_score_for_big_files()
    assert RESULT, 'Plagiarism checker not working'
