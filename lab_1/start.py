"""
Concordance implementation starter
"""
import os
import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    stop_words = stop_words.split ('\n')


    #  here goes your logic: calling methods from concordance.py

    tokens = main.tokenize(data)
    print('tokens:', tokens[:10])

    tokens = main.remove_stop_words(tokens, stop_words)
    print('tokens without stop words:', tokens[:10])

    freq_dict = main.calculate_frequencies(tokens[:10])
    print('frequencies for the first element:', freq_dict[tokens[0]])

    top_3_words = main.get_top_n_words(freq_dict, 3)
    print('top 3 words:', top_3_words)

    concordance = main.get_concordance(tokens, 'time', 1, 2)
    print('get_concordance for "time"', concordance[:5])

    adjacent_words = main.get_adjacent_words(tokens, 'time', 1, 2)
    print('get_adjacent_words for "time"', adjacent_words[:5])

    sorted_concordance = main.sort_concordance(tokens, 'time', 2, 3, True)
    print('sorted_concordance:', sorted_concordance[0])

    main.write_to_file('report.txt', sorted_concordance)

    RESULT = sorted_concordance

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'
