"""
Concordance implementation starter
"""

from main import read_from_file
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import get_concordance
from main import get_adjacent_words
from main import write_to_file
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    text = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file((os.path.join(current_dir, 'stop_words.txt')))
    stop_words = stop_words.split('\n')
    tokens = tokenize(text)

    tokens = remove_stop_words(tokens, stop_words)
    print('Tokens without stopwords: {}'.format(tokens))

    freq_dict = calculate_frequencies(tokens)
    print('Frequencies of tokenize words: {}'.format(freq_dict))

    top_words = get_top_n_words(freq_dict, 5)
    print('5 most popular words: {}'.format(top_words))

    concordance = get_concordance(tokens, 'sodium', 1, 1)
    print('Getting concordance for the token "sodium": {}'.format(concordance))

    adjacent_words = get_adjacent_words(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                                         'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad'], 'happy', 2, 3)
    print('Adjacent words for word "happy": {} '.format(adjacent_words))

    write_to_file = write_to_file('report.txt', concordance)

    RESULT = write_to_file
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'
