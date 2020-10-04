"""
Concordance implementation starter
"""

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))

    #  here goes your logic: calling methods from main.py
    data =read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file(os.path.join(current_dir, 'stop_words.txt')).split()

    tokens = tokenize(data)
    tokens_without_stop_words = remove_stop_words(tokens, stop_words)
    tokens_frequencies = calculate_frequencies(tokens_without_stop_words)
    print("\n")
    print(f"top 10 words from data.txt: {get_top_n_words(tokens_frequencies, 10)}")
    print(f"top 50-100 words from data.txt: {get_top_n_words(tokens_frequencies, 100)[50:]}")

    contexts_without_stop_words = get_concordance(tokens, 'mom', 10, 10)
    contexts_stop_words = get_concordance(tokens_without_stop_words, 'mom', 10, 10)
    print("\n")
    print(f"contexts with stop words: {contexts_stop_words}")
    print(f"contexts_without_stop_words: {contexts_stop_words}")

    adjacent_words_king = get_adjacent_words(tokens_without_stop_words, 'king', 1, 1)
    adjacent_words_queen = get_adjacent_words(tokens_without_stop_words, 'queen', 1, 1)
    print("\n")
    print(f"frame for king: {adjacent_words_king}")
    print(f"frame for queen: {adjacent_words_queen}")

    sort_words_dog = sort_concordance(tokens_without_stop_words, 'dog', 2, 2, True)
    sort_words_cat = sort_concordance(tokens_without_stop_words, 'cat', 2, 2, True)
    print("\n")
    print(f"left context sort for dog: {sort_words_dog}")
    print(f"right context sort for cat: {sort_words_cat}")

    write_to_file(os.path.join(current_dir, 'adjacent_king.txt'), adjacent_words_king)
    write_to_file(os.path.join(current_dir, 'adjacent_queen.txt'), adjacent_words_queen)

    RESULT = contexts_without_stop_words
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'


    # #  use data.txt file to test your program
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # data = read_from_file(os.path.join(current_dir, 'data.txt'))
    # stop_words = []
    #
    # #  here goes your logic: calling methods from concordance.py
    #
    # RESULT = None
    # # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT == [(), ()], 'Concordance not working'