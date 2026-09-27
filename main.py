import math
import heapq
from tqdm import tqdm
import csv

# preprocessing
f = open("words.txt")
f = list(f)
words = set([x.strip() for x in f])

r_entropy = 0
total_entropy = math.log(len(words), 2)

result_keeper = {} # "0": ['v', 'r'], etc...

round = 1

def getArgWords(k): 
    words_entropy = []
    for word in words:
        heapq.heappush(words_entropy, (-getEntropy(word), word))
    
    top_k_words = []
    for i in range(min(k, len(words_entropy))):
        word = heapq.heappop(words_entropy)
        top_k_words.append((word[1], -word[0]))

    return top_k_words

def getEntropy(guess):
    results = getResults(guess)[0] # list of 243 elements
    bits = 0
    for result in results:
        p = result / len(words)
        if p != 0:
            bits += p * math.log(1 / p, 2)
    
    return bits

def getResults(guess):
    # iterate through the set of possible words, assign each word a result where the result is what the guess should have been to witness this word
    res = [set() for _ in range(3 ** 5)]
    for word in words: 
        result = 0

        word_pos = {}
        for i in range(len(word)):
            if word[i] in word_pos:
                word_pos[word[i]].add(i)
            else:
                word_pos[word[i]] = {i}

        remaining_pos = set(range(len(word)))
        # determining green tiles
        for i in range(len(guess)):
            if guess[i] == word[i]:
                result += 2 * (3 ** (len(word) - i - 1))
                word_pos[guess[i]].remove(i)
                remaining_pos.remove(i)
        
        # determining yellow tiles
        for i in remaining_pos:
            if guess[i] in word_pos and word_pos[guess[i]]:
                result += 1 * (3 ** (len(word) - i - 1))
                word_pos[guess[i]].pop()

        res[result].add(word)
    
    return list(map(len, res)), res


def getNumResult(result):
    res = 0
    for i in range(len(result)-1, -1, -1):
        res += int(result[i]) * (3 ** (len(result) - i - 1))
    
    return res

def preprocess():
    with open("words_to_entropy.txt", "w") as f:
        max_heap = []
        for word in tqdm(words):
            heapq.heappush(max_heap, (-getEntropy(word), word))

        while max_heap:
            c = heapq.heappop(max_heap)
            word, entropy = c[1], -c[0]
            f.writelines(f"{word},{entropy}\n")

def printArgWords(arr):
    print(f"==========================TOP {len(arr)} BEST WORDS BASED ON ENTROPY==========================")
    for i in range(len(arr)):
        print(f"{i}. {arr[i][0]} (Bits: {arr[i][1]})") # 1. pizza (Bits: 3.1415)
    print("================================================================================================")


def sortEntropy():
    res = []
    with open("words_to_entropy.txt", "r") as f:
        data = csv.reader(f)
        for row in data:
            res.append((row[1], row[0]))

def printFirstEntropy(k):

    print(f"==========================TOP {k} BEST WORDS BASED ON ENTROPY==========================")
    with open("words_to_entropy.txt", "r") as f:
        for i in range(k):
            line = f.readline().strip().split(',')
            print(f"{i}. {line[0]} (Bits: {line[1]})") # 1. pizza (Bits: 3.1415)
    
    print("================================================================================================")

if __name__ == "__main__":
    #preprocess()

    while round <= 6 and len(words) > 1:

        print(f"CURRENT ENTROPY: {r_entropy}")

        if round == 1:
            printFirstEntropy(10)
        else:
            argwords = getArgWords(10) # gets the top ten best words to guess based on entropy
            printArgWords(argwords)

        # user guesses
        guess = input("Enter your guess: ")
        result = input("Enter results (0: gray, 1: yellow, 2: green): ")

        round += 1
        
        counts, buckets = getResults(guess)
        p = counts[getNumResult(result)] / len(words)
        if p:
            r_entropy += math.log(1/p , 2)
        else:
            print("No possible word.")
            break
        
        words = buckets[getNumResult(result)]







