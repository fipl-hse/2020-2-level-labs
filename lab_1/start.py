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
    print('Tokens: ', tokens[:20])

    tokens = main.remove_stop_words(tokens, stop_words)
    print('Tokens without stop words: ', tokens[:20])

    freq_dict = main.calculate_frequencies(tokens)
    print('Frequency for the first word: ', freq_dict[tokens[0]])

    top_n_words = main.get_top_n_words(freq_dict, 5)
    print('Top 5 words: ', top_n_words)

    concordance = main.get_concordance(tokens, 'time', 2, 3)
    print('Concordance for "time":', concordance[:6])

    adjacent_words = main.get_adjacent_words(tokens, 'time', 2, 3)
    print('Adjacent words for "time":', adjacent_words)

    main.write_to_file('report.text', concordance)

    RESULT = concordance

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'
