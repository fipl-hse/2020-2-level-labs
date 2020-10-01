"""
Concordance implementation starter
"""
import os
import main

if __name__ == '__main__':

    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt')).split('\n')

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print("tokens:", tokens[:13])

    tokens = main.remove_stop_words(tokens, stop_words)
    print("tokens without stop words:", tokens[:10])

    freq_dict = main.calculate_frequencies(tokens[:10])
    print("frequency for the first word:", freq_dict[tokens[0]])

    top_2_words = main.get_top_n_words(freq_dict, 2)
    print("top 2 words:", top_2_words)

    concordance = main.get_concordance(tokens, 'team', 1, 2)
    print("concordance for 'team':", concordance[:3])

    adjacent_words = main.get_adjacent_words(tokens, 'team', 1, 2)
    print("adjacent words for word 'team':", adjacent_words[:3])

    RESULT = concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['time', 'a'], ['time', 'years'], ['olympic', 'great']], 'Concordance not working'
