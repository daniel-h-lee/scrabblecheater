import sys
import csv
from collections import Counter
import heapq

SCORES  = {'A': 1, 'C': 3, 'B': 3, 'E': 1, 'D': 2, 'G': 2,
         'F': 4, 'I': 1, 'H': 4, 'K': 5, 'J': 8, 'M': 3,
         'L': 1, 'O': 1, 'N': 1, 'Q': 10, 'P': 3, 'S': 1,
         'R': 1, 'U': 1, 'T': 1, 'W': 4, 'V': 4, 'Y': 4,
         'X': 8, 'Z': 10}


NUM_WILDCARDS = sys.argv[1].count('@')
HAND_CHAR = sys.argv[1].replace('@', '')
HAND_CHAR = HAND_CHAR.upper()
HAND_COUNT = Counter(HAND_CHAR)


# print(NUM_WILDCARDS, HAND_CHAR, HAND_COUNT)

def word_generator():
    with open('sowpods.txt','r') as f: # open by default mode='r' (read)
        reader = csv.reader(f)
        for line in reader:
            yield line[0]

def score(word):
    ''' (str) -> int
    Return the score of a word, taking into account the wildecards (0)'''
    return sum((min(HAND_COUNT.get(c, 0), word.count(c)) * SCORES[c] for c in set(word)))

def is_word(word):
    ''' (str) -> bool
    Return True taking the wildecards into account
    '''
    used_wildecards = 0
    for c in set(word):
        used_wildecards +=  max(word.count(c) - HAND_COUNT.get(c, 0), 0)
        if used_wildecards > NUM_WILDCARDS:
            return False
    return True

def cheater_generator():
    ''' () -> generator
    Returns a generator of pairs (score, word)
    '''
    for word in word_generator():
        if is_word(word):
            yield (-score(word), word)


if __name__ == '__main__':
    result = []
    for pair in cheater_generator():
        heapq.heappush(result, pair)

    for i in range(min(len(result), 10)):
        minus_score, word = heapq.heappop(result)
        print(abs(minus_score), word)
