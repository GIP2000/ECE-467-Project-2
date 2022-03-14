#!/usr/bin/python3

# from functools import map
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

        wc = len(self.words)

        self.table = [[[] for _ in range(wc)] for _ in range(wc)]
        for i,word in enumerate(self.words):
            self.table[i][i] = grammer.terminal[word]

        # loop through diagonals
        for i in range(1,wc):
            self.__check_diagnal(i)
    
    def __check_diagnal(self,d_loc:int):
        seconds = [(self.table[d_loc][d_loc],d_loc,d_loc)]
        for y in range(d_loc-1,-1,-1):
            for x in range(d_loc-1,-1,-1):
                if len(self.table[y][x]) == 0: continue
                second_adder = []
                for second,ly,lx in seconds:
                    for combo,fw,sw in Table.__make_strings(self.table[y][x],second):
                        if combo in self.grammer.non_terminal:
                            self.table[ly][d_loc] += map(
                                lambda v: (v,(y,x,fw),(ly,lx,sw)),
                                self.grammer.non_terminal[combo])
                            second_adder.append(( self.table[ly][d_loc][0],ly,d_loc))
                seconds += second_adder 

    @staticmethod 
    def __make_strings(first,second):
        for fw in first:
            for sw in second:
                yield f"{fw} {sw}",fw,sw

def get_input() -> str:
    return input('Input a sentence\ntype "quit" to quit the application\n')

if __name__ == "__main__":
    grammer = Grammer.make_grammer("sampleGrammar.cnf")
    sentence = get_input()
    while sentence != "quit":
        t = Table(grammer,sentence)
        sentence = get_input()

