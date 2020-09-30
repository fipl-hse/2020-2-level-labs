"""
Concordance implementation starter
"""



from main import *
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []
    print('What does this program do?')
    print(f'It reads texts: {data[:50]}...')
    tokens = remove_stop_words(tokenize(data), stop_words)
    print(f'It tokenizes it: {tokens[:100]}')
    frequencies = calculate_frequencies(tokens)
    print(f'It also count how many times a word appears in text. '
          f'For instance, the word "year" appears '
          f'there {frequencies["year"]} times')
    top = get_top_n_words(frequencies, 20)
    print(f'It can also provide you with as many top-frequent words as you '
          f'wish. For example, here are the first 20: {", ".join(top)}.')
    concordance = sort_concordance(tokens, 'year', 3, 5, True)
    contexts = []
    for example in concordance[:10]:
        context = " ".join(example)
        contexts.append(context)
    contexts = "\n".join(contexts)
    print(f'Finally, you can access 10 first contexts in which a certain '
          f'word appeard using this prog. Here is all the contexts for '
          f'word "year":\n{contexts}')
    print('What do we mean by "first"? Well, they are all sorted!' 
          'Notice that they appear in a alphabetical order.'
          ' And even reversed.')
    adj_words = get_adjacent_words(tokens, 'year', 3, 5)
    pairs = []
    for words in adj_words[:10]:
        pair = " ".join(words)
        pairs.append(pair)
    pairs = "\n".join(pairs)
    print(f'We can also get adjacted words! Here are some of them for "year":\n{pairs}')
    RESULT = sort_concordance(tokens, 'end', 3, 5, True)
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'
