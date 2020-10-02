"""
Concordance implementation starter
"""
import os
from main import read_from_file
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import get_concordance


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    text = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file(os.path.join(current_dir,'stop_words.txt')).split('\n')     #all what was in main s_w get i & make list

    #  here goes your logic: calling methods from concordance.py

    tokens = tokenize(text)
    print('The fist 20 tokens: ', tokens[:20])

    tokens = remove_stop_words(tokens, stop_words)
    print('30 tokens without stop words: ', tokens[:30])

    freq_dict = calculate_frequencies(tokens)
    print('frequency of 5 first words: ', freq_dict[tokens[:5]])

    top_list = get_top_n_words(freq_dict, 3)
    print('3 most popular words: ', top_list )

    concordance = get_concordance(tokens, 'entire', 2, 3)
    print('concordance for "entire":', concordance)


    RESULT = concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT ==  'Concordance not working'
