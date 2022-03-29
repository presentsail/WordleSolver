'''
Script to return possible words for the game Wordle.
author: presentsail
version: 3.2.2
'''
from itertools import islice

if type(fiveLet) == tuple:
    fiveLetBackup = fiveLet
else:
    fiveLetBackup = fiveLet.copy()

def askAction(actThree=False):
    '''
    Ask user for action, check if input is one of the options
    '''
    options = {"1": "use word",
               "2": "reroll",
               "3": "display more results",
               "4": "manually chose word",
               "5": "end program",
               }
    # If there's only one qualifying word, don't offer to reroll
    if len(results) == 1:
        del options["2"]
        del options["3"]
    # If more than one result displayed, user pick word
    if actThree:
        del options["1"]
        del options["2"]
    # If all results have been displayed
    if not results:
        del options["3"]

    # Display options
    for option, instruction in options.items():
        print(f'({option}) - {instruction}')
        
    while True:
        
        answer = input("Enter number:  ")

        if answer in options:
            return answer

        print("Error: Invalid input")

def askEval():
    '''
    For evaluation function. Check if input is valid, return input.
    '''
    while True:
        evaluation = input(f'Enter colors for word {result}:  ')
        evaluation = evaluation.lower()

        if len(evaluation) == 5:
            
            for let in evaluation:
                # checkfor letter other than g y b
                if let not in {"g","y","b"}:
                    break
                
                # if no other letter found
                else:
                    return evaluation
                
        # if length != 5 or contains letter other than g y b
        print("Error: Invalid input")

def evaluate():
    '''
    Fills lists for green, yellow, and black letters according to
    Wordle colors.
    '''
    greenLets.clear()

    # ask user for colors given by Wordle
    evaluation = askEval()
    
    for i, (evalLet, resultLet) in enumerate(zip(evaluation, result)):
        if evalLet == "g":
            greenLets.append(resultLet)

        else:
            greenLets.append("")

        if evalLet == "y":
            yellowLets.add(resultLet)
            yellowPlaces[i].add(resultLet)

        if evalLet == "b":
            blackLets.add(resultLet)

def getTopHit():
    '''Return the qualifying word with the highest score'''
    # Pick word with highest score
    result = max(results, key=results.get)
    # Get score
    resultScore = max(results.values())
    
    # Print number of qualifying words
    hits = f'\n{len(results)} results found'
    print(hits)
    # Print word and its score
    topHit = f'{result} {resultScore}\n'
    print(topHit)

    return result

# How many times a letter appears in five letter words in words.txt
# compared to the letter that appears the least
points = {'s': 61, 'e': 61, 'a': 52, 'r': 39, 'o': 38, 'i': 34,
          'l': 32, 't': 30, 'n': 26, 'd': 23, 'u': 22, 'c': 19,
          'p': 18, 'y': 18, 'm': 17, 'h': 16, 'g': 14, 'b': 14,
          'k': 11, 'f': 10, 'w': 9, 'v': 6, 'z': 2, 'x': 2,
          'j': 2, 'q': 1
          }

greenLets = []      # location of green letters
yellowLets = set()  # set of yellow letters
yellowPlaces = dict([(i, set()) for i in range(5)])
                    # dict of positions [1,5] with sets of letters
blackLets = set()   # list of black letters

results = {}        # dict of qualifying words and number of points

result = ""

attempts = 1

fiveLet = []

with open("words.txt",'r') as wordsfile:
    

while True:
    wordsfile = fiveLet
    for line in wordsfile:
        line = line.strip()

        # only check 5 letter words
        if len(line) == 5:

            score = 0

            for i, (greenLet, lineLet) in (
                enumerate(zip(greenLets, line))):

                if (
                    # letters don't match green letters
                    (greenLet != "" and greenLet != lineLet)
                    # yellow letters in bad place
                    or (lineLet in yellowPlaces[i])
                    # blacklisted letters are in word
                    or (lineLet in blackLets)
                ):
                    # disqualify word
                    score = -1

            # check if all yellow letters are present
            for let in yellowLets:
                if let not in line:
                    score = -1

            # if word hasn't been disqualified
            if score != -1:
                # add word to dict of qualifiers
                results[line] = 0

    # Assign score to each qualifying word
    for word in results:
        repeat = []

        for let in word:
            # If letter has not already appeared in word
            if let not in repeat:
                results[word] += points[let]
                repeat += let
            # If it has, take away points
            else:
                results[word] -= points[let]
    
    results = dict(sorted(
        results.items(),
        key=lambda item: item[1],
        reverse=True
    ))

    result = getTopHit()

    fiveLet = tuple(results.keys())

    action = -1
    while True:
        # Ask user what they want to do
        action = askAction(actThree = action=="3")

        # Use most recent result
        if action == "1":
            evaluate()
            break

        # Bring up another result
        elif action == "2":
            del results[result]
            
            result = getTopHit()

        # Display the top 5 results
        elif action == "3":
            sortSlice = dict(islice(results.items(), 5))
            print(f"\n{sortSlice}\n")
            # Remove top 5 from results
            [results.pop(key) for key in sortSlice.keys()]

        # Use a word other than the most recent result
        elif action == "4":
            result = input("Enter word:  ")
            result = result.lower()
            evaluate()
            break

        # Stop playing
        elif action == "5":
            break

    # If Wordle has been solved, end program
    if "" not in greenLets or action == "5":
        print(f"Program ended on {attempts} attempts")
        fiveLet = fiveLetBackup
        break

    attempts += 1
    results.clear()
