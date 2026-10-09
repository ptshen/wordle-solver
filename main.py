import heapq
import math
from tqdm import tqdm

possible_words = set()

def preprocess():
    global possible_words
    with open('words.txt', 'r') as f:
        lines = f.readlines()
    
    possible_words = set(map(lambda x: x.strip(), lines))

def compute_word_entropies():
    preprocess()
    with open('words_entropies.txt', 'w') as f: 
        f.writelines('word,entropy\n')

        for word in tqdm(possible_words):
            f.writelines(f"{word},{get_entropy(word)}\n")

def sort_word_entropies():
    h = []
    with open("words_entropies.txt", 'r') as f:
        lines = f.readlines()[1:]
        for line in lines: 
            word, entropy = line.split(',')
            entropy = float(entropy)
            heapq.heappush(h, (-entropy, word))
        
    with open("sorted_words_entropies.txt", 'w') as f:
        f.writelines('word,entropy\n')
        for entropy, word in h:
            f.writelines(f"{word},{-entropy}\n")

def print_initial_word_entropies(k): # loads top k initial word entropies 
    with open("sorted_words_entropies.txt", 'r') as f:
        lines = f.readlines()[1:]

    print(f"====================TOP {k} WORDS====================\n")
    
    for i in range(min(k, len(lines))):
        line = lines[i]
        word, entropy = line.split(',')
        print(f"{word}: {entropy}")
    
    print(f"=====================================================")

def print_top_k_words(k):
    top_k_words = []
    for word in possible_words:
        #print(word)
        heapq.heappush(top_k_words, (-get_entropy(word), word))
    
    top_k_words = top_k_words[:min(k, len(top_k_words))]

    print(f"====================TOP {k} WORDS====================\n")

    for i in range(len(top_k_words)):
        entropy, word = top_k_words[i]
        print(f"{word}: {-entropy}\n")

    print(f"=====================================================")

def get_entropy(guess):
    entropy = 0
    states = [0] * (3**5)

    for word in possible_words:
        state = get_state(guess, word)
        states[state] += 1

    probabilities = list(map(lambda x: x/len(possible_words), states))
    
    for prob in probabilities: 
        if prob > 0: 
            entropy += prob * math.log(1 / prob, 2)
    
    return entropy

def get_state(guess, word):
    state = 0
    n = len(guess)
    
    g_rem, w_rem = {}, {}
    for i in range(n):
        g_rem[i] = guess[i]
        w_rem[i] = word[i]

    # account for green tiles
    for i in range(n):
        if guess[i] == word[i]:
            state += 2 * (3 ** (n-i-1))
            del g_rem[i]
            del w_rem[i]
    
    """# g_rem = {1: g, 3: e, 4: v, 5: v}, w_rem = {1: v, 3: v, 4: e, 5: l }"""
    ignore_set = set()
    for pg, vg in g_rem.items():
        for pw, vw in w_rem.items():
            if pw not in ignore_set and pg != pw and vg == vw:
                state += 1 * 3 ** (n-pg-1)
                ignore_set.add(pw)
                break
    
    return state

def update_possible_words(guess, result):
    global possible_words
    updated_possible_words = set()
    for word in possible_words:
        if valid_state(guess, result, word):
            updated_possible_words.add(word)
    
    possible_words = updated_possible_words

def valid_state(guess, result, word):
    n = len(guess)
    
    consider_letters = {}

    for i in range(n):
        consider_letters[i] = word[i]

    # fail greens
    for i in range(n):
        if result[i] == "2":
            if guess[i] != word[i]:
                return False 

            del consider_letters[i]
    
    # fail yellows 
    for i in range(n):
        if result[i] == "1":
            if guess[i] == word[i] or guess[i] not in consider_letters.values():
                return False

            del consider_letters[i]
    
    # fail grays
    for i in range(n):
        if result[i] == "0" and guess[i] in consider_letters.values():
            return False
    
    return True

def game():
    round = 1
    preprocess()
    print(f"Size of Wordle word list: {len(possible_words)}")
    print_initial_word_entropies(10)
    while round <= 6: 

        if round > 1: 
            print_top_k_words(10)

        guess = input("Enter your guess: ")
        result = input("Enter the result: ")

        update_possible_words(guess, result)
        round += 1
        print('\n\n')

if __name__ == "__main__":   
    game()


