#wordle expanded program

import random



#use asterisks for blank spaces
#use all blank spaces if pattern unknown
##pattern = input("Word has pattern:  ")
##contains = input("Word contains in any position:  ")
##blacklist = input("Word does not contain:  ")
pattern = "*****"
contains = ""
blacklist = ""

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
            if pattern == "":
                pattern = "*****"
            
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
                

    while True:
        #list of top 10 most common letters
        topten = ['s', 'e', 'a', 'r', 'o', 'i', 'l', 't', 'n', 'd']
        topten = {'s':4331//1611, 'e':4303//1611, 'a':3665//1611,
                  'r':2733//1611, 'o':2712//1611, 'i':2428//1611,
                  'l':2293//1611, 't':2154//1611, 'n':1867//1611, 'd':1}
        #initialize list of scores for each word in results
        resultscores = []
        
        for i in range(len(results)):
            word = results[i]
            resultscores.append(0)
            repeat = ""

            for let in word:
                if let in topten:
                    if let not in repeat:
                        resultscores[-1] += topten[let]
                        repeat += let
                    else:
                        resultscores[-1] -= 2
                        
        result = results[resultscores.index(max(resultscores))]
        print("%d results found" % len(results))
        print(result,max(resultscores))

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

                        
