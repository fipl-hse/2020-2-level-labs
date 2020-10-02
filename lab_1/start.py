"""
Concordance implementation starter
"""
import os
from main import read_from_file, get_stop_words, calculate_frequencies
from main import tokenize, remove_stop_words, get_top_n_words, write_to_file
from main import get_concordance, get_adjacent_words, sort_concordance


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py
    tokens = tokenize(data) # токенезирование
    stop_words = get_stop_words()
    # токены без стоп слов
    tokens_clean = remove_stop_words(tokens, stop_words)
    # частоты токенов
    freq_dict = calculate_frequencies(tokens_clean)
    # слово для поиска
    top_words = get_top_n_words(freq_dict, "mom", 10, 10)
    print("top 10 words {}".format(top_words))

    result_normal_concordance = get_concordance(tokens_clean, "mom", 3, 2)
    result_adjacent_concordance = get_adjacent_words(tokens, "mom", 3, 2)
    result_sorted_concordance = sort_concordance(tokens, "mom", 3, 2, True)
    print(f"normal concordance: {result_normal_concordance}, "
          f"adjacent concordance: {result_adjacent_concordance}, "
          f"sorted concordance: {result_sorted_concordance}")

    write_to_file(os.path.join(current_dir, 'concordance.txt'), result_normal_concordance)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert result_normal_concordance, 'Concordance not working'
