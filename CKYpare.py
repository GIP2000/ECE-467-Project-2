#!/usr/bin/python3

from functools import reduce
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk import download as n_download
n_download("punkt")

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
            input_file = input("Enter the path of the input file")
        
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
        for gsdx in range(1,self.wc): 
            for sdy in range(0,self.wc-gsdx):
                sdx = gsdx+sdy
                for dx in range(gsdx,0,-1):
                    # dy is the compliment 
                    dy = (gsdx+1)-dx
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

        def __make_bracket(ty:int,tx:int,tz:int,tab_amount:int = 1) -> str:
            if not tree_mode:
                tab_amount = 0

            if ty == tx:
                return f"{' '*tab_amount}[{self.table[ty][tx][tz]} {self.words[ty]}]"
            (name,f,s) = self.table[ty][tx][tz]
            return f"{' '*tab_amount}[{name}{newline if tree_mode else ' '}{__make_bracket(f[0],f[1],f[3],tab_amount+1)}{newline if tree_mode else ' '}{__make_bracket(s[0],s[1],s[3],tab_amount+1)}{newline + (' '*tab_amount) if tree_mode else ''}]"

        for parse_count,(_,first,second) in enumerate(S_arr):
            print(f"Valid parse #{parse_count+1}:")
            print(f"[S{newline if tree_mode else ' '}{__make_bracket(first[0],first[1],first[3])}{newline if tree_mode else ' '}{__make_bracket(second[0],second[1],second[3])}{newline if tree_mode else ''}]")

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
    grammer = Grammer.make_grammer("sampleGrammar.cnf")
    
    val = input("Do you want textual parse trees to be displayed (y/n)?:")
    while val != 'y' and val != 'n':
        val = input("Do you want textual parse trees to be displayed (y/n)?:")
    val = val == 'y'
    sentence = get_input()
    while sentence != "quit":
        t = Table(grammer,sentence)
        if val:
            t.outputPermutations(True)
        t.outputPermutations()
        sentence = get_input()
    print("Goodbye!")

