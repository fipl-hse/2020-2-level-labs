
import main
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    text = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file((os.path.join(current_dir, 'stop_words.txt')))
    stop_words = stop_words.split('\n')

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(text)
    
    RESULT = None
    tokens = main.tokenize(text)
    print("tokens:", tokens[:15])

    tokens_stop_words = main.remove_stop_words(tokens, stop_words)
    print("tokens without stop words:", tokens_stop_words[:7])

    frequencies = main.calculate_frequencies(tokens)
    print('frequencies for the word: ', frequencies[tokens[2]])

    top_words = main.get_top_n_words(freq_dict, 3)
    print("top words:", top_words)

    concordance = main.get_concordance(tokens, 'time', 1, 3)
    print(" concordance:", concordance[:3])

RESULT = concordance[:3]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['of', 'time', 'team', 'presented', 'a'], ['in', 'time', 'team', 'over', 'the'], ['the', 'time', 'a', 'stalin', 'directive']]
