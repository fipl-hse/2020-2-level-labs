"""
Concordance implementation starter
"""


import os
import main


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []
    print('What does this program do?')
    print(f'It reads texts: {data[:50]}...')
    tokens = main.remove_stop_words(main.tokenize(data), stop_words)
    print(f'It tokenizes it: {tokens[:100]}')
    frequencies = main.calculate_frequencies(tokens)
    print(f'It also count how many times a word appears in text. '
          f'For instance, the word "year" appears '
          f'there {frequencies["year"]} times')
    top = main.get_top_n_words(frequencies, 20)
    print(f'It can also provide you with as many top-frequent words as you '
          f'wish. For example, here are the first 20: {", ".join(top)}.')
    concordance = main.sort_concordance(tokens, 'year', 3, 5, True)
    CONTEXTS = []
    for example in concordance[:10]:
        CONTEXT = " ".join(example)
        CONTEXTS.append(CONTEXT)
    CONTEXTS = "\n".join(CONTEXTS)
    print(f'Finally, you can access 10 first contexts in which a certain '
          f'word appeard using this prog. Here is all the contexts for '
          f'word "year":\n{CONTEXTS}')
    print('What do we mean by "first"? Well, they are all sorted!'
          'Notice that they appear in a alphabetical order.'
          ' And even reversed.')
    adj_words = main.get_adjacent_words(tokens, 'year', 3, 5)
    PAIRS = []
    for words in adj_words[:10]:
        PAIR = " ".join(words)
        PAIRS.append(PAIR)
    PAIRS = "\n".join(PAIRS)
    print(f'We can also get adjacted words! Here are some of them for "year":\n{PAIRS}')
    RESULT = main.sort_concordance(tokens, 'end', 3, 5, True)[:10]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['an', 'unusually', 'early', 'end', 'to', 'his', 'career', 'in', 'the'],
                      ['and', 'sometimes', 'they', 'end', 'them', 'literally', 'with', 'carved', 'wisps'],
                      ['and', 'towards', 'the', 'end', 'of', 'that', 'century', 'a', 'number'],
                      ['army', 'at', 'the', 'end', 'of', 'the', 'season', 'the', 'vfl'],
                      ['at', 'the', 'northwestern', 'end', 'of', 'the', 'island', 'although', 'the'],
                      ['at', 'the', 'other', 'end', 'the', 'two', 'men', 'were', 'arrested'],
                      ['atoms', 'at', 'the', 'end', 'of', 'guerrilla', 'forces', 'numbered', 'no'],
                      ['babylonians', 'at', 'the', 'end', 'of', 'the', 'reading', 'his', 'friends'],
                      ['beach', 'at', 'the', 'end', 'of', 'la', 'dolce', 'vita', 'has'],
                      ['birthday', 'to', 'the', 'end', 'of', 'the', 'year', 'its', 'one']], 'Concordance not working'
