"""
Concordance implementation starter
"""
import os
import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt')).split()
    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('Tokens:', tokens[:20])

    tokens_stop_words = main.remove_stop_words(tokens, stop_words)
    print('Tokens without stop words:', tokens_stop_words[:20])

    tokens = main.remove_stop_words(tokens, stop_words)
    print('tokens without stop words:', tokens[:10])

    tokens_frequencies = main.calculate_frequencies(tokens_stop_words[:20])
    print('Frequency of the first word:', tokens_frequencies[tokens_stop_words[0]])

    top = main.get_top_n_words(tokens_frequencies, 20)
    print('Top 20 words:', top)

    concordance = main.get_concordance(tokens, 'task', 2, 1)
    print("Concordance for word 'task':", concordance[:6])

    adjacent_words = main.get_adjacent_words(tokens, "task", 2, 3)
    print("Adjacent words for word 'task':", adjacent_words)

    main.write_to_file('report.txt', top)

    RESULT = top
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'
