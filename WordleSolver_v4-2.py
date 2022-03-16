fiveLet = set()
with open('words.txt','r') as f:
    for line in f:
        line = line.strip()
        if len(line) == 5:
            fiveLet.add(line)
            
from itertools import islice

class WordleSolver:
    
    def __init__(self, infile):
        self.points = {'s': 61, 'e': 61, 'a': 52, 'r': 39, 'o': 38, 'i': 34,
                       'l': 32, 't': 30, 'n': 26, 'd': 23, 'u': 22, 'c': 19,
                       'p': 18, 'y': 18, 'm': 17, 'h': 16, 'g': 14, 'b': 14,
                       'k': 11, 'f': 10, 'w': 9, 'v': 6, 'z': 2, 'x': 2,
                       'j': 2, 'q': 1
                       }

        self.infile = infile

        self.green = []
        self.yellow = dict([(i, set()) for i in range(5)])
        self.cum_yel = set()
        self.black = set()

        self.results = {}
        self.result = ""
        self.resultScore = 0

        self.action = -1

        self.attempts = 1

        self.run()

    def __str__(self):
        string = f'green: {self.green}\nyellow: {self.yellow}\n{self.cum_yel}\nblack: {self.black}\n'
        return string

    def findQuali(self):
        self.results.clear()

        for word in self.infile:
            score = 0
            for i, (grnLet, wrdLet) in (
                enumerate(zip(self.green, word))
            ):
                if (
                    (grnLet != '' and grnLet != wrdLet)
                    or (wrdLet in self.yellow[i])
                    or (wrdLet in self.black)
                ):
                    score = -1

            for yelLet in self.cum_yel:
                if yelLet not in word:
                    score = -1

            if score != -1:
                self.results[word] = 0

        print(f'\n{len(self.results)} results found')

    def assignScore(self):
        for word in self.results:
            repeat = set()
            for let in word:
                if let not in repeat:
                    self.results[word] += self.points[let]
                    repeat.add(let)
                else:
                    self.results[word] -= self.points[let]

        self.results = dict(sorted(
            self.results.items(),
            key=lambda item: item[1],
            reverse=True,
        ))

    def getTopHit(self):
        '''Sets, prints, and returns top hit'''
        self.result = max(self.results, key=self.results.get)
        self.resultScore = max(self.results.values())
        print(self.result, self.resultScore, '\n')
        return self.result

    def evaluate(self, colors, word):
        '''Sets instance attrs according to given colors'''
        self.green.clear()
        for i, (c, w) in enumerate(zip(colors, word)):
            if c == 'g':
                self.green.append(w)
            else:
                self.green.append('')

            if c == 'y':
                self.yellow[i].add(w)

            if c == 'b':
                self.black.add(w)

        self.cum_yel = set.union(*self.yellow.values())

    def askAction(self, actThree=False):
        options = {"1": "use word",
                   "2": "reroll",
                   "3": "display more results",
                   "4": "manually chose word",
                   "5": "end program",
                   }

        if len(self.results) == 1:
            del options['2']
            del options['3']

        if actThree:
            del options['1']
            del options['2']

        if not self.results:
            del options['3']

        for option, instruction in options.items():
            print(f'({option}) - {instruction}')

        while True:
            answer = input('Enter number: ')
            if answer in options:
                self.action = answer
                return self.action

            print('Error: Invalid input')

    def askEval(self):
        while True:
            evl = input(f'Enter colors for word {self.result}:  ')
            evl = evl.lower()

            if len(evl) == 5:
                for let in evl:
                    if let not in {'g','y','b',}:
                        break
                    else:
                        return evl
            print('Error: Invalid input')

    def askWord(self):
        '''Asks for and returns word entered by user'''
        while True:
            word = input('Enter word:  ')
            word = word.lower()

            if len(word) == 5:
                return word

            print('Error: Word must be 5 letters')

    def checkCont(self):
        if (self.green and '' not in self.green) or self.action == '5':
            print(f'Program ended on {self.attempts} attempts')
            return False
        return True

    def getTopFive(self):
        '''Prints and removes top five results'''
        resultSlice = dict(islice(self.results.items(), 5))
        print(f'\n{resultSlice}\n')
        [self.results.pop(key) for key in resultSlice.keys()]

    def run(self):
        while True:
            self.findQuali()
            self.assignScore()
            self.getTopHit()
            while True:
                self.action = self.askAction(actThree=self.action=='3')

                if self.action == '1':
                    self.evaluate(self.askEval(), self.result)
                    break

                elif self.action == '2':
                    del self.results[self.result]
                    self.getTopHit()

                elif self.action == '3':
                    self.getTopFive()

                elif self.action == '4':
                    self.result = self.askWord()
                    self.evaluate(self.askEval(), self.result)
                    break
                
                elif self.action == '5':
                    break

            if not self.checkCont():
                break

            self.attempts += 1

app = WordleSolver(fiveLet)
