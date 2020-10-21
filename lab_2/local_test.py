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
        f'{origin_text} \n\n'
        f'and \n\n'
        f'{susp_text}: \n\n'
        f'{lcs_lenght} \n')

    matrix = main.fill_lcs_matrix(origin_tokens, susp_tokens)
    print(f'A matrix:')
    print(*matrix, sep='\n', end='\n\n')

    longest_lcs = main.find_lcs(origin_tokens, susp_tokens, matrix)
    print(f'The longest common subsequence: {longest_lcs}')

    score = main.calculate_plagiarism_score(lcs_lenght, susp_tokens)
    print(f'The plagiarism score: {score:.2f}\n')

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

    print(f'The text plagiarism score for \n\n'
        f'{origin_text} \n'
        f'\n and \n\n'
        f'{susp_text}: \n\n'
        f'{score:.2f}\n\n')

def test_find_diff():
    origin_text = 'a big cat loves a small cat'
    susp_text = 'a dog loves a cat'

    origin_tokens = tokenize(origin_text)
    susp_tokens = tokenize(susp_text)

    matrix = main.fill_lcs_matrix(origin_tokens, susp_tokens)

    lcs = main.find_lcs(origin_tokens, susp_tokens, matrix)

    difference = main.find_diff_in_sentence(origin_tokens, susp_tokens, lcs)

    print(f'The difference indexes between \n\n'
        f'{origin_text} \n'
        f'\n and \n\n'
        f'{susp_text}: \n\n'
        f'{difference}')

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

    print(f'The accumulated main statistics for pairs of sentences in texts: \n\n'
        f'{origin_text} \n'
        f'\n and \n\n'
        f'{susp_text}: \n')
    print(*stat.items(), sep='\n', end='\n\n')

    report = main.create_diff_report(origin_tokens,
                                     susp_tokens,
                                     stat)
    print(f'A report:\n\n{report}\n')


#test_till_calculate_plagiarism_score()
#test_calculate_text_plagiarism_score()
#test_find_diff()
#test_accumulated_stat_and_report()
