"""Backus-Naur Form Tool

This class allows the user to instantiate a GrammarBuddyHelper object which allows
the creation of grammar using Backus-Naur Form notation. It is assumed that the 
the rules of the grammar are compiled within a list with each definition constituting a line.

This class accepts text files (.txt) and the default save location is within BNF Forms/grammar.txt.

...

Attributes
----------
rules : str[]
    every definition of each symbol within the grammar as a list with the structure ['symbol symDelim expression', ...]
langMap : {str : str[]}
    a dictionary of the grammar which is in the form of {symbol : [expression, ...], ...}
symDelim : str
    the syntax used to delimit the symbols from the expressions (default ::=)
exprDelim : str
    the syntax used to delimit the expressions from each other (default |)

Methods
-------
generate(symbol)
    this function generates an expression given a symbol
contains(term)
    this function determines whether or not a given term is either a symbol or expression
addSymbol(symbol)
    this function determines whether or not a symbol is within the grammar and adds it if not
addExpression(symbol, expression)
    this function determines whether or not an expression represents a symbol and adds the expression if not
saveMap(filename='BNF Forms/grammar.txt')
    this function saves the current grammar as a text file
Written by Kody L. Robinson 2025
"""
import random, sys
import pyinputplus as pyip

class GrammarBuddyHelper:
    def __init__(self, rules, symDelim='::=', exprDelim='|'):
        """
        This is the default constructor, custom delimiters can be used with '::=' and '|' 
        representing the default delimiters for the symbols and expressions respectively
        ...

        Parameters
        ----------
        rules : str[]
            every definition of each symbol within the grammar as a list with the structure ['symbol symDelim expression', ...]
        symDelim : str
            the syntax used to delimit the symbols from the expressions (default ::=)
        exprDelim : str
            the syntax used to delimit the expressions from each other (default |)

        Returns
        ----------
        langMap : { str: str[] }
            a dictionary of the grammar which is in the form of { symbol : [expression] }
            
        """
        if not rules:
            print("!WARNING: Rule set cannot be empty")
        self.symDelim = symDelim
        self.exprDelim = exprDelim
        self.langMap = {}
        for i in rules:
            if symDelim not in i:
                print("Malformed rule: " + i)
                return
            line = i.split(symDelim)
            expressions = line[1].split(exprDelim)
            rule = {line[0]: expressions}
            self.langMap.update(rule)
   
    def generate(self, symbol):
        """
        This method generates an expression based upon a given symbol. 
        Returns "Symbol not found in grammar" if the given symbol is not found within the grammar
        ...

        Parameters
        ----------
        symbol : str
            this is the symbol that will be substituted with a randomly selected expression

        Returns
        -------
        term : str
            this is the expresssion that was generated for the symbol
        """
        term = ''
        if symbol not in self.langMap:
            term = "Symbol not found in grammar: " + symbol
            return term
        rule = self.langMap[symbol]
        expression = rule[random.randint(0, len(rule)-1)]
        iterableExpressions = expression.split(' ')
        for i in iterableExpressions:
            if i in self.langMap:
                term += self.generate(i).strip() + ' '
            else:
                term += i + ' '
        return term

    def contains(self, term):
        """
        This method checks whether or not a term is a symbol. If the term is not a symbol, all of the 
        expressions of each symbol are checked
        ...

        Parameters
        ----------
        term : str
            this is the given term to be searched. Can be a symbol or expression

        Returns
        -------
        bool
            an unnamed boolean value representing whether or not the term was found within the grammar
        """
        if term in self.langMap.keys():
            return True
        for i in self.langMap.values():
            if term in i:
                return True
        return False

    def addSymbol(self, symbol):
        """
        This method checks whether or not a given symbol is within the grammar. If not, the symbol is added
        ...

        Parameters
        ----------
        symbol : str
            this is the symbol to be added
        """
        add = {symbol: []}
        self.langMap.update(add)

    def addExpression(self, symbol, expression):
        """
        This method checks whether or not a given expression is found for the given symbol. If not,
        the symbol is defined as the expression and is saved into the grammar
        ...

        Parameters
        ----------
        symbol : str
            this is the symbol in which the expression is to be added under
        expression : str
            this is the expression to be added 
        """
        if symbol in self.langMap:
            self.langMap[symbol].append(expression)
        else:
            self.addSymbol(symbol)
            self.langMap.update({symbol: [expression]})

    def saveMap(self, filename='BNF Forms/grammar.txt'):
        """
        This method allows the grammar to be saved in a text file with each line constituting a symbol defintion
        ...

        Parameters
        ----------
        filename : str
            the filename that the grammar will be saved as        
        """
        if '.txt' not in filename:
            filename += '.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            for k in self.langMap.keys():
                line = k + self.symDelim
                for v in self.langMap[k]:
                    if v == self.langMap[k][-1]:
                        line += v
                    else:    
                        line += v + self.exprDelim
                file.write(line + '\n')
        file.close()         

    def updateMap(self, filename):
        if '.txt' not in filename:
            filename += '.txt'
        with open(filename, 'r', encoding='utf-8') as file:
            for rule in file:
                self.addSymbol(rule.split(self.symDelim)[0])
                for expr in rule.split(self.symDelim)[1].split(self.exprDelim):
                    self.addExpression(rule.split(self.symDelim)[0], expr)

def main():
    rules = [] # Empty list to hold grammar

    try:
        with open("BNF Forms/math.txt", 'r') as file:
            for line in file:
                rules.append(line.strip())
    except FileNotFoundError as e:
        print(f"Uh oh\n{e}")
    gb = GrammarBuddyHelper(rules) # Constructing GrammarBuddyHelper object

    gb.addExpression('<x>','<s>') # Adding sample expression
    for i in range(100):
        print(f'{i+1}: {gb.generate('<expression>')}') # Generate 100 sample expressions
    gb.saveMap("BNF Forms/testgrammar.txt") # Saving updated grammar

if __name__ == "__main__":
    rules = []
    start = pyip.inputYesNo("Would you like to load a grammar file? Press ENTER to exit\n", blank=True) 
    if start == 'yes':
        while not rules:
            filename = input("Path of grammar file? Press ENTER to skip\n")
            if not filename:
                break
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    for line in file:
                        rules.append(line.strip())
                gb = GrammarBuddyHelper(rules)
            except FileNotFoundError as e:
                print(f"Uh oh \n{e}\n")
    elif not start:
        sys.exit()
    else:
        gb = GrammarBuddyHelper([])
    flag = True
    while flag:
        choice = pyip.inputMenu(['Generate a symbol', 'List symbols', 'Add a symbol', 'Add an expression', 'Does it contain?', 'Open a grammar text file', 'Save grammar to a text file', 'Exit'], numbered=True)

        match choice:
            case 'Generate a symbol':
                if 0 == len(gb.langMap.keys()): 
                    print("Cannot generate a big nothing symbol!")
                    continue
                print("Press ENTER to skip")
                choice = pyip.inputMenu(list(gb.langMap.keys()), numbered=True, blank=True)
                print(gb.generate(choice))
            case 'List symbols':
                for i in gb.langMap.keys():
                    print(i)
            case 'Add a symbol':
                symbol = input("What symbol would you like to add?\n")
                gb.addSymbol(symbol)
            case 'Add an expression':
                symbol = input("What symbol does this expression define?\n")
                expression = input("What is the expression?\n")
                gb.addExpression(symbol=symbol, expression=expression)
            case 'Does it contain?':
                term = input("What term would you like to check?\n")
                print(gb.contains(term))
            case 'Open a grammar text file':
                filename = input("What is the name of the text file you would like to open? Press ENTER to exit\n")
                if filename:
                    try:
                        gb.updateMap(filename)
                    except Exception as e:
                        print(f'Uh oh\n{e}')
            case 'Save grammar to a text file':
                filename = input("What name would you like to save the file as? Press ENTER to exit\n")
                if filename:
                    try:
                        gb.saveMap(filename)
                    except Exception as e:
                        print(f'Uh oh \n{e}')
            case 'Exit':
                flag = False
