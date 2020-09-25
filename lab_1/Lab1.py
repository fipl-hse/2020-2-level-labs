import re

def tokenize(f):
        try:
                tokens = []
                for line in f:
                        for word in re.findall(r"[a-zA-z]+", line):
                                
                                tokens.append(word.lower())
        except TypeError:
                tokens = []
        return set(tokens)

def remove_stop_words(f, stop_words_way):
        try:  
                stop_words = tokenize(stop_words_way)
                tokens = tokenize(f)
                tokens = tokens - stop_words
                return list(tokens)
        except TypeError:
                tokens = []
                
        
        
        

        

        
            
f = open('data.txt', 'r')
stop_words =  open('stop_words.txt', 'r')     
tokens_with_out_stop_words = remove_stop_words(f, stop_words)
stop_words.close()
f.close()




