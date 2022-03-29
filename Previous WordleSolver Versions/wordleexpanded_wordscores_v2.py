#wordle expanded program

import random


#------------------------------Initialize variables-----------------------------
#use asterisks for blank spaces
#use all blank spaces if pattern unknown

#location of green letters
pattern = "*****"
#string of yellow letters
contains = ""
#string of black letters
blacklist = ""
#list of locations of yellow letters
notpatlist = []

#initialize list of qualifying words
results = []
    

while True:
    wordsfile = open("words.txt",'r')
    for line in wordsfile:
        line = line.strip()

        #only check 5 letter words
        if len(line) != 5: pass

        else:
            score = 0

            #check if words follows pattern
            pattern = pattern.ljust(5,"*")
            
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

                
                
#--------------------------------Display guesses--------------------------------
    while True:
        points = {'s': 61, 'e': 61, 'a': 52, 'r': 39, 'o': 38, 'i': 34,
                  'l': 32, 't': 30, 'n': 26, 'd': 23, 'u': 22, 'c': 19,
                  'p': 18, 'y': 18, 'm': 17, 'h': 16, 'g': 14, 'b': 14,
                  'k': 11, 'f': 10, 'w': 9, 'v': 6, 'z': 2, 'x': 2,
                  'j': 2, 'q': 1}
        #initialize list of scores for each word in results
        resultscores = []
        
        for i in range(len(results)):
            word = results[i]
            resultscores.append(0)
            repeat = ""

            for let in word:
                if let in points:
                    if let not in repeat:
                        resultscores[-1] += points[let]
                        repeat += let
                    else:
                        resultscores[-1] -= points[let]
                        
        result = results[ resultscores.index( max(resultscores) ) ]
        print("%d results found" % len(results))
        print(result)

        if len(results) > 1:
            reroll = input("Reroll? y/n:  ")
            if reroll == "y":
                results.remove(result)
            elif reroll == "all":
                print(results)
                break
            else:
                break
        else:
            break
        

#----------------------------Ask if guess is correct----------------------------
    cont = input("Correct? y/n:  ")
    if cont == "y":
        again = input("Play again? y/n:  ")
        if again == "y":
            pattern = "*****"
            contains = ""
            blacklist = ""
        else:
            break

    repat = input("Word has pattern:  ")
    if repat != "":
        pattern = repat.strip()

    recon = input("New yellow letters:  ")
    if recon != "":
        contains += recon.strip()

    reblack = input("New black letters:  ")
    if reblack != "":
        blacklist += reblack.strip()
        for let in blacklist:
            if let in pattern:
                blacklist = blacklist.replace(let,"")
                

    renotpat = input("Position of yellow letters:  ")
    if renotpat != "":
        notpatlist.append(renotpat.strip())

    results = []
    wordsfile.close()

                        
