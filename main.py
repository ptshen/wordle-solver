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
    for i in range(k):
        word = heapq.heappop(words_entropy)
        top_k_words.append((word[1], -word[0]))

    return top_k_words

def getEntropy(guess):
    states = [] # 3 ** 5
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    for e in range(3):
                        a, b, c, d, e = str(a), str(b), str(c), str(d), str(e)
                        states.append(a + b + c + d + e)
    
    bits = 0
    for result in states:
        if nonZeroProb(guess, result):
            p, h = getProb(guess, result), getBits(guess, result)
            info = p * h
            print(guess, result, p, h)
            bits += info
    
    return bits


def nonZeroProb(guess, result):
    # check known green characters and see if result is gray on any of those characters
    gray, yellow, green = set(), set(), set()
    for i in range(len(result)):
        if result[i] == "0":
            gray.add(guess[i])
        elif result[i] == "1":
            yellow.add(guess[i])
        elif result[i] == "2":
            green.add(guess[i])

    for green_char in green:
        if green_char in result_keeper.get("0", []):
            return False
    
    for yellow_char in yellow:
        if yellow_char in result_keeper.get("0", []):
            return False
    
    return True


def updateResult(guess, result):
    for i in range(len(result)):
        if result[i] not in result_keeper:
            result_keeper[result[i]] = set()

        result_keeper[result[i]].add(guess[i])



def getProb(guess, result):
    words_after_guess = set()

    for word in words:
       # check green pos
        n, can_add = len(word), True
        for i in range(n):
            if result[i] == "2":
                if word[i] != guess[i]:
                    can_add = False
        
        # check yellow
        gray_pos = {}
        for i in range(n):
            if result[i] == "0":
                gray_pos[word[i]] = gray_pos.get(word[i], []) + [i]

        #print(word, gray_pos)
        
        for i in range(n):
            if result[i] == "1":
                
                if guess[i] == word[i]:
                    can_add = False

                if guess[i] in gray_pos:
                    if len(gray_pos[guess[i]]) == 0:
                        can_add = False
                    else:
                        del gray_pos[guess[i]][0]
                else:
                    can_add = False
        
        # check gray
        for i in range(n):
            if result[i] == "0":
                if guess[i] in gray_pos:
                    can_add = False

        if can_add:
            words_after_guess.add(word)               
    
    #print(words_after_guess)
    return len(words_after_guess) / len(words)

def getBits(guess, result):
    prob = getProb(guess, result)
    if prob == 0:
        return 0
    
    return math.log(1 / prob, 2)

def preprocess():
    with open("words_to_entropy.txt", "w") as f:
        for word in tqdm(words):
            f.writelines(f"{word},{getEntropy(word)}\n")

        

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
    with open("words_to_entropy_sorted.txt", "r") as f:
        for i in range(len(k)):
            print(f.readline())



if __name__ == "__main__":
    #getBits("pizza", "22201")
    #print(getProb("cohoe", "20000"))

    preprocess()
    # print(getProb("cohoe", "00001"))
    # print(getEntropy("cohoe"))
    
    # print(getEntropy("rossa"))
    # print(getProb("rossa", "01000"))

    # while round <= 6 and r_entropy < total_entropy:

    #     if round == 1:
    #         printFirstEntropy()
    #     else:
    #         argwords = getArgWords(1) # gets the top ten best words to guess based on entropy
        
    #     printArgWords(argwords)

    #     # user guesses

    #     guess = input("Enter your guess: ")
    #     result = input("Enter results (0: gray, 1: yellow, 2: green): ")
    #     updateResult(guess, result)

    #     round += 1
    #     r_entropy = getBits(guess, result)







