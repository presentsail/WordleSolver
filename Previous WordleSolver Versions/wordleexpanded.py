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
                
    try:
        answer = random.choice(results)
        print("%d results found" % len(results))
        print(answer)
        while True:
            reroll = input("Reroll? y/n:  ")
            if reroll == "y":
                answer = random.choice(results)
                print("%d results found" % len(results))
                print(answer)
            else:
                break
            
    except:
        print(results)


        

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

                        
