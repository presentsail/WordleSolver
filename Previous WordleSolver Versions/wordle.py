#Wordle

import random

wordsfile = open("words.txt",'r')

#use asterisks for blank spaces
#use all blank spaces if pattern unknown
pattern = input("Word has pattern:  ")
contains = input("Word contains in any position:  ")
blacklist = input("Word does not contain:  ")

notpatlist = []

while True:
    notpat = input("Letters in wrong position:  ")
    if notpat == "done": break

    else:
        notpatlist.append(notpat)

#initialize list of qualifying words
results = []

if pattern == "":
    pattern = "*****"

if notpat == "":
    notpat = "*****"

for line in wordsfile:
    line = line.strip()

    #only check 5 letter words
    if len(line) != 5: pass
    

    else:
        score = 0

        #check if word follows pattern
        for let in range(5):
            if pattern[let] == "*":
                pass
            else:
                if pattern[let] != line[let]:
                    score = -1

            for pat in notpatlist:
                if pat[let] == line[let]:
                    score = -1
                    
        #check if word contains desired letters
        for let in contains:
            if let not in line:
                score = -1

        #check for blacklisted letters
        for let in blacklist:
            if let in line:
                score = -1

            
                    
        if score == 0:
            results.append(line)

print(random.choice(results))
