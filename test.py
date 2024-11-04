nombre = 'Fernando'.upper()

def get_next_consonant(word):
    vowels = 'AEIOU'

    for i in word:
        if i in vowels:
            return i



print(get_next_consonant(word=nombre[1:]))