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

def calculate_frequencies(tokens, text, stop_words_way):
        dictionary = {}
        #print(text)
        for i in tokens:
                #print(i)
                dictionary[i] = text.count(i)
        print(dictionary)
        return dictionary
                
        
        
        
        

        

        
            
with open('data.txt', 'r') as f:
        with open('stop_words.txt', 'r') as stop_words:

                tokens_with_out_stop_words = remove_stop_words(f, stop_words)
                text = tokenize(f)
                calculate_frequencies(tokens_with_out_stop_words, text, stop_words)





