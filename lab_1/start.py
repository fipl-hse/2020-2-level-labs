"""
Concordance implementation starter
"""
import os
import main


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    stop_words = stop_words.split ('\n')


    #  here goes your logic: calling methods from concordance.py

    tokens = main.tokenize(data)
    print('tokenize:', tokens[:10])

    RESULT = None

    tokens = main.remove_stop_words(tokens, stop_words)
    print('remove_stop_words:', tokens[:10])

    freq_dict = main.calculate_frequencies(tokens[:10])
    print('calculate_frequencies, first elem:', freq_dict[tokens[0]])

    top_3_words = main.get_top_n_words(freq_dict, 3)
    print('top 3 words:', top_3_words)

    concordance = main.get_concordance(tokens, 'rocket', 1, 2)
    print('get_concordance for "team"', concordance[:3])

    adjacent_words = main.get_adjacent_words(tokens, 'rocket', 1, 2)
    print('get_adjacent_words for "team"', adjacent_words[:3])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'
