# Make a set of five letter words from file
fiveLet = set()
with open('words.txt','r') as f:
    for line in f:
        line = line.strip()
        if len(line) == 5:
            fiveLet.add(line)
            
from itertools import islice
from collections import Counter

class WordleSolver:

    points = {
        's': 61, 'e': 61, 'a': 52, 'r': 39, 'o': 38, 'i': 34,
        'l': 32, 't': 30, 'n': 26, 'd': 23, 'u': 22, 'c': 19,
        'p': 18, 'y': 18, 'm': 17, 'h': 16, 'g': 14, 'b': 14,
        'k': 11, 'f': 10, 'w': 9, 'v': 6, 'z': 2, 'x': 2,
        'j': 2, 'q': 1
    }
    
    def __init__(
        self, 
        infile:iter, 
        wordlength:int = 5, 
        resetpoints:bool = False,
    ):
        '''
        Initiates WordleSolver instance attributes and runs run method.

        :param infile: Iterable of words to be searched through.
                       All words should be the length specified
                       in wordlength.

        :param wordlength: Length of words that to be put in Wordle.
                           Defaults to 5.

        :param resetpoints: Whether or not to reinitialize how words are
                            scored based on words in infile.
        '''
        self.infile = infile
        if resetpoints:
            self.setpoints()

        self.length = wordlength

        self.green = []
        self.yellow = {position: set() for position in range(self.length)}
        self.cum_yel = set()
        self.black = set()

        self.results = {}
        self.result = ""
        self.topscore = 0

        self.action = -1

        self.attempts = 1

        self.run()

    def __str__(self):
        string = (f'green: {self.green}\n'
                  + f'yellow: {self.yellow}\n'
                  + f'{self.cum_yel}\n'
                  + f'black: {self.black}\n')
        return string

    def findqualifiers(self):
        '''Fills results with words that meet Wordle requiremets.'''
        self.results.clear()

        for word in self.infile:
            score = 0
            for i, (greenlet, wordlet) in (
                enumerate(zip(self.green, word))
            ):
                if (
                    (greenlet != '' and greenlet != wordlet)
                    or (wordlet in self.yellow[i])
                    or (wordlet in self.black)
                ):
                    score = -1

            for yellowlet in self.cum_yel:
                if yellowlet not in word:
                    score = -1

            if score != -1:
                self.results[word] = 0

        print(f'\n{len(self.results)} results found')

    def assignscores(self):
        '''Gives each word in results a score based on its letters.'''
        for word in self.results:
            self.results[word] = 0
            lets_present = set()
            for let in word:
                if let not in lets_present:
                    self.results[word] += self.points[let]
                    lets_present.add(let)
                else:
                    self.results[word] -= self.points[let]

        self.results = dict(sorted(
            self.results.items(),
            key=lambda item: item[1],
            reverse=True,
        ))

    def gettophit(self) -> str:
        '''Sets, prints, and returns result with highest value.'''
        self.result = max(self.results, key=self.results.get)
        self.topscore = max(self.results.values())
        print(self.result, self.topscore, '\n')
        return self.result

    def evaluate(self, colors: str, word: str):
        '''Sets instance attributes according to given colors.'''
        self.green.clear()
        for i, (c, w) in enumerate(zip(colors, word)):
            if c == 'g':
                self.green.append(w)
                if c in self.black:
                    self.black.remove(c)
            else:
                self.green.append('')

            if c == 'y':
                self.yellow[i].add(w)
                if c in self.black:
                    self.black.remove(c)

            if c == 'b' and c not in self.green and c not in self.yellow:
                self.black.add(w)

        self.cum_yel = set.union(*self.yellow.values())

    def askaction(self, prevact3:bool=False) -> str:
        '''
        Determines available actions, displays them, and asks user
        what they want to do.

        :param prevact3: Whether or not the user previously selected
                         action 3.
        '''
        options = {"1": "use word",
                   "2": "reroll",
                   "3": "display more results",
                   "4": "manually chose word",
                   "5": "end program",
                   }

        if len(self.results) == 1:
            del options['2']
            del options['3']

        if prevact3:
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

    def askeval(self) -> str:
        '''Asks user for and returns colors given by Wordle'''
        while True:
            evl = input(f'Enter colors for word {self.result}:  ')
            evl = evl.lower()

            if len(evl) == self.length:
                for let in evl:
                    if let not in {'g','y','b',}:
                        break
                else:
                    return evl
            print('Error: Invalid input')

    def askword(self) -> str:
        '''Asks for and returns word entered by user'''
        while True:
            word = input('Enter word:  ')
            word = word.lower()

            if len(word) == self.length:
                return word

            print(f'Error: Word must be {self.length} letters')

    def checkcont(self) -> bool:
        '''Checks if program should be ended'''
        if (self.green and '' not in self.green) or self.action == '5':
            print(f'Program ended on {self.attempts} attempts')
            return False
        return True

    def gettopfive(self) -> dict:
        '''Prints and removes top five results'''
        result_slice = dict(islice(self.results.items(), 5))
        print(f'\n{result_slice}\n')
        [self.results.pop(key) for key in result_slice.keys()]
        return result_slice

    def run(self):
        while True:
            self.findqualifiers()
            self.assignscores()
            self.gettophit()
            while True:
                self.action = self.askaction(prevact3=self.action=='3')

                if self.action == '1':
                    self.evaluate(self.askeval(), self.result)
                    break

                elif self.action == '2':
                    del self.results[self.result]
                    self.gettophit()

                elif self.action == '3':
                    self.gettopfive()

                elif self.action == '4':
                    self.result = self.askword()
                    self.evaluate(self.askeval(), self.result)
                    break
                
                elif self.action == '5':
                    break

            if not self.checkcont():
                break

            self.attempts += 1

    def setpoints(self):
        '''Resets the points attribute according to words in infile.'''
        all_lets = []
        for word in self.infile:
            all_lets += list(word)
        let_count = dict(Counter(all_lets))
        minimum = min(let_count.values())
        for let in let_count:
            let_count[let] //= minimum

        let_count = dict(sorted(
            let_count.items(),
            key=lambda item: item[1],
            reverse=True,
        ))
        self.points = let_count

app = WordleSolver(fiveLet)
