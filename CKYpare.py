#!/usr/bin/python3

from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk import download as n_download
n_download("punkt",quiet=True)

class Grammer: 

    def __init__(self) -> None:
        self.non_terminal = defaultdict(lambda : [])
        self.terminal = defaultdict(lambda : [])

    def insert(self, rule, result):
        if " " in result:
            self.non_terminal[result].append(rule)  
        else:
            self.terminal[result].append(rule)
    
    @staticmethod
    def make_grammer(input_file: str = None):
        if input_file is None:
            input_file = input("Enter the path of the input file: ")
        
        grammer = Grammer()

        with open(input_file, 'r') as g_file: 
            for line in g_file:
                [rule,result] = line.split("-->")
                grammer.insert(rule.strip(), result.strip())

        return grammer


class Table: 
    def __init__(self, grammer: Grammer, sentence: str) -> None:
        self.words = word_tokenize(sentence)
        self.grammer = grammer
        self.wc = len(self.words)
        self.table = [[[] for _ in range(self.wc)] for _ in range(self.wc)]


        # populate terminals 
        for i,word in enumerate(self.words):
            self.table[i][i] = grammer.terminal[word]

        # loop through diagonals and populate non_terminals 
        for gsdx in range(1,self.wc): # gsdx is which diagnal were doing 
            for sdy in range(0,self.wc-gsdx): # the value of y in the diagnal 
                sdx = gsdx+sdy # sdx is the value of x in the diagnal 
                for dx in range(gsdx,0,-1): # the diff in x for the x area we are checking for teh first non-terminal
                    # dy is the compliment 
                    dy = (gsdx+1)-dx # the diff in y for the y area we are checking 

                    # gets every of first and second non-terminals 
                    for combo,fw,i_f,sw,i_s in Table.__make_strings(self.table[sdy][sdx-dx], self.table[sdy+dy][sdx]): 
                        self.table[sdy][sdx] += map(
                            lambda val: (val,(sdy,sdx-dx,fw,i_f), (sdy+dy,sdx,sw,i_s)) # adds backpointers
                            ,self.grammer.non_terminal[combo])
    

    def outputPermutations(self,tree_mode: bool = False) -> None: 
        S_arr = [val for val in self.table[0][self.wc-1] if val[0] == "S"]
        if len(S_arr) <= 0:
            print("Invalid Sentence")
            return

        newline = '\n'
        print(f"Number of valid parses: {len(S_arr)}")

        def __make_bracket(ty:int,tx:int,tz:int,tm:bool = False,tab_amount:int = 1) -> str:
            if not tm:
                tab_amount = 0

            if ty == tx:
                return f"{' '*tab_amount}[{self.table[ty][tx][tz]} {self.words[ty]}]"
            (name,f,s) = self.table[ty][tx][tz]
            return f"{' '*tab_amount}[{name}{newline if tm else ' '}{__make_bracket(f[0],f[1],f[3],tm,tab_amount+1)}{newline if tm else ' '}{__make_bracket(s[0],s[1],s[3],tm,tab_amount+1)}{newline + (' '*tab_amount) if tm else ''}]"

        for parse_count,x in enumerate(S_arr):
            if not isinstance(x,tuple):
                print(f"[{x} {self.words[0]}]")
                if tree_mode:
                    print(f"[{x} {self.words[0]}]")
                return 
            (_,first,second) = x
            print(f"Valid parse #{parse_count+1}:")
            print(f"[S {__make_bracket(first[0],first[1],first[3],False)} {__make_bracket(second[0],second[1],second[3],False)}]")
            if tree_mode:
                print(f"[S{newline}{__make_bracket(first[0],first[1],first[3],True)}{newline}{__make_bracket(second[0],second[1],second[3],True)}{newline}]")

    @staticmethod 
    def __make_strings(first,second):
        first = [val if not isinstance(val,tuple) else val[0] for val in first]
        second = [val if not isinstance(val,tuple) else val[0] for val in second]
        for i_f,fw in enumerate(first):
            for i_s,sw in enumerate(second):
                yield f"{fw} {sw}",fw,i_f,sw,i_s

def get_input() -> str:
    return input('Input a sentence\ntype "quit" to quit the application\n')

if __name__ == "__main__":
    print("Loading Grammer...")
    grammer = Grammer.make_grammer()
    
    val = input("Do you want textual parse trees to be displayed (y/n)?:")
    while val != 'y' and val != 'n':
        val = input("Do you want textual parse trees to be displayed (y/n)?:")
    val = val == 'y'
    sentence = get_input()
    while sentence != "quit":
        t = Table(grammer,sentence)
        t.outputPermutations(val)
        sentence = get_input()
    print("Goodbye!")


