import re

def tokenize(f):
        try:
                tokens = []
                for line in f:
                        for word in re.findall(r"[a-zA-z]+", line):
                                
                                tokens.append(word.lower())
                return tokens
        except TypeError:
                tokens = []
        

def remove_stop_words(f, stop_words_way):
        try:  
                stop_words = set(tokenize(stop_words_way))
                tokens = set(tokenize(f))
                tokens = tokens - stop_words
                return list(tokens)
        except TypeError:
                print(tokens)

def most_popular(dictionary, n):
    ans = []
    cnt = 0
    for w in sorted(dictionary, key=dictionary.get, reverse=True):
        ans.append(w)
        cnt += 1
        # print(cnt)
        if (cnt == n):
            # print(ans)
            return ans


with open('data.txt', 'r') as f:
    with open('stop_words.txt', 'r') as stop_words:
        tokenize_text = tokenize(f)
        tokens_with_out_stop_words = remove_stop_words(tokenize_text, stop_words)
        dictionary = calculate_frequencies(tokenize_text, tokens_with_out_stop_words)
        most_popular(dictionary, 10)
