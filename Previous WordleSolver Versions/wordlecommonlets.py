#Find the how many times each letter in the alphabet appears in all five
#letter words in words.txt

wordsfile = open("words.txt",'r')

#initialize dictionary of letters and number of appearances
stats = {}

#fill dictionary
for line in wordsfile:
    line = line.strip()

    #only check 5-letter words
    if len(line) == 5:
        for let in line:
            if let in stats:
                stats[let] += 1
            else:
                stats[let] = 1

print(stats,"\n")

wordsfile.close()


#initiallize list of letters and list of appearances
common = [] #letters in order of most common to least
comnum = [] #number of appearances from most to least

#
for i in range( len(stats) ):
    maxcount = 0
    maxlet = ""
    for key in stats:
        if stats[key] > maxcount:
            maxcount = stats[key]
            maxlet = key
    common.append(maxlet)
    comnum.append(stats.pop(maxlet))


topten = common[:10]
print(topten)
topnum = comnum[:10]
print(topnum)



#make dict of letters and amount of appearances proportional to each other
points = {}
for let in common:
    num = common.index(let)
    points[let] = comnum[num]//comnum[-1]
print("Points:", points)

###-----------------------------------------------
##lis = ['ricin', 'lysin', 'punny', 'dangs', 'quest']
##
##lis2 = []
##
##for i in range(len(lis)):
##    lis2.append(0)
##    word = lis[i]
##    p = ""
##    
##    for let in word:
##        if let in topten and let not in p:
##            lis2[-1] += 1
##            p += let
##            
##
##print(lis)
##print(lis2)
##
##
##result = lis[lis2.index(max(lis2))]
##print(result)

#find two words which combined contain all lets in topten

wordsfile = open("words.txt",'r')

qualify = []
for line in wordsfile:
    line = line.strip()
    if len(line) == 5:
        score = 0
        r = ''
        for let in line:
            if let in r:
                score = -1
            else:
                r += let
            if let not in topten:
                score = -1
        if score != -1:
            qualify.append(line)

wordsfile.close()


score = 0
pair = []
esc = False
#take a word
for word in qualify:
    
    if len(pair) == 2:
        break
    
    topten = ['s', 'e', 'a', 'r', 'o', 'i', 'l', 't', 'n', 'd']
    for let in word:
        topten.remove(let)



    remaining = topten
    for other in qualify:
        score = 0
        for let2 in other:
            if let2 not in remaining:
                score = -1

        if score != -1:
            print(word,other)

print(pair)
    
