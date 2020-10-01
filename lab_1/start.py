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
    print('tokens:', tokens[:10])

    tokens_stop_words = main.remove_stop_words(tokens, stop_words)
    print('tokens without stop words:', tokens_stop_words[:10])

    tokens_frequencies = main.calculate_frequencies(tokens_stop_words[:10])
    print('frequency of the first word:', tokens_frequencies[tokens_stop_words[0]])

    top = main.get_top_n_words(tokens_frequencies, 3)
    print('Top 3 words:', top)

    concordance = main.get_concordance(tokens, 'team', 1, 2)
    print("concordance for word 'team':", concordance[:3])

    adjacent_words = main.get_adjacent_words(tokens, 'team', 1, 2)
    print("adjacent words for word 'team':", adjacent_words[:3])

    sorts_concordance = main.sort_concordance(tokens, 'team', 1, 2, True)
    print("sorted concordance for word 'team':", sorts_concordance[:4])

    main.write_to_file('report.txt', sorts_concordance)

    RESULT = concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'
