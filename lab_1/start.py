"""
Concordance implementation starter
"""

from main import read_from_file
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('tokens: ', tokens[:6])

    frequencies = main.calculate.frequences(tokens)
    print('frequencies of the word: ', frequencies[tokens[:6]])

    top_n = main.get_top_n_words(frequencies,10)
    print('top of 10 words: ', top_n)

    concordance = main.get_concordance(tokens, 'people', 2, 3)
    print('concordance for the word: ', concordance[:6])

    adjacent_words = main.get_adjacent_words (tokens, 'peopla',5, 5)
    print('adjacent words for the word: ', adjacent_words[:3])

    write_file = ('report.txt', adjacent_words)

    RESULT = None
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'
