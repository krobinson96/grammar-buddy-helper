"""Backus-Naur Form Tool

This class allows the user to instantiate a GrammarBuddyHelper object which allows
the creation of grammar using Backus-Naur Form notation. It is assumed that the 
the rules of the grammar are compiled within a list with each definition constituting a line.

This class accepts text files (.txt) and the default save location is within BNF Forms/grammar.txt.

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
updateMap(filename='BNF Forms/grammar.txt')
    this function updates the current grammar from a text file
Written by Kody L. Robinson 2025
"""
import random, sys
import pyinputplus as pyip

class GrammarBuddyHelper:
    def __init__(self, rules, symDelim='::=', exprDelim='|'):
        """
        This is the default constructor, custom delimiters can be used with '::=' and '|' 
        representing the default delimiters for the symbols and expressions respectively

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
            if not exprDelim in rule and not line[0]:
                print("Empty definition ...")
                continue
            self.langMap.update(rule)
   
    def generate(self, symbol):
        """
        This method generates an expression based upon a given symbol. 
        Returns "Symbol not found in grammar" if the given symbol is not found within the grammar

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

        Parameters
        ----------
        term : str
            this is the given term to be searched. Can be a symbol or expression

        Returns
        -------
        bool
            an unnamed boolean value representing whether or not the term was found within the grammar
        """
        if term in self.langMap.keys() and term:
            return f"{term} is a symbol."
        else:
            for i in self.langMap.keys():
                for j in self.langMap[i]:
                    if term in j:
                        return f"{term} is an expression."
        return "{term} is not present within the grammar."

    def addSymbol(self, symbol):
        """
        This method checks whether or not a given symbol is within the grammar. If not, the symbol is added

        Parameters
        ----------
        symbol : str
            this is the symbol to be added
        """
        if symbol in self.langMap.keys():    
            choice = pyip.inputYesNo("Symbol {symbol} is already in the grammar. Would you like to overwrite it?\n", blank=True)
            if choice != 'no':
                add = {symbol: []}
                self.langMap.update(add)
        else:
            add = {symbol: []}
            self.langMap.update(add)
    def addExpression(self, symbol, expression):
        """
        This method checks whether or not a given expression is found for the given symbol. If not,
        the symbol is defined as the expression and is saved into the grammar

        Parameters
        ----------
        symbol : str
            this is the symbol in which the expression is to be added under
        expression : str
            this is the expression to be added 
        """
        if symbol in self.langMap and expression not in self.langMap[symbol]:
            self.langMap[symbol].append(expression)
        elif symbol not in self.langMap:
            self.addSymbol(symbol)
            self.langMap[symbol].append(expression)
        else:
            print(f'Expression {expression} is already in the map under {symbol}!')

    def saveMap(self, filename='BNF Forms/grammar.txt'):
        """
        This method allows the grammar to be saved in a text file with each line constituting a symbol defintion

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
                file.write(line+"\n")
        file.close()         

    def updateMap(self, filename):
        """
        This method allows the current grammar to be updated with a given filename
        
        Parameters
        ----------
        filename : str 
            the filename that the grammar will be saved as 
        """
        if '.txt' not in filename:
            filename += '.txt'    
        with open(filename, 'r', encoding='utf-8') as file:
            for rule in file:
                for expr in rule.strip().split(self.symDelim)[1].split(self.exprDelim):
                    self.addExpression(rule.strip().split(self.symDelim)[0].strip(), expr.strip())

def main():
    rules = [] # Empty list to hold grammar

    try:
        with open("BNF Forms/math.txt", 'r') as file:
            for line in file:
                rules.append(line.strip())
    except FileNotFoundError as e:
        print(f"Uh oh\n{e}")
    gb = GrammarBuddyHelper(rules) # Constructing GrammarBuddyHelper object

    gb.addExpression('<x>','<expression>') # Adding sample expression
    for i in range(100):
        print(f'{i+1}: {gb.generate('<x>')}') # Generate 100 sample expressions
    gb.saveMap("BNF Forms/testgrammar.txt") # Saving updated grammar

if __name__ == "__main__":
    rules = []
    start = pyip.inputYesNo("Would you like to load a grammar file? Press ENTER to exit\n", blank=True) 
    if start == 'yes':
        while not rules:
            filename = input("Path of grammar file? Press ENTER to skip\n")
            if not filename:
                gb = GrammarBuddyHelper([])
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
        choice = pyip.inputMenu(['Generate a symbol', 'Generate a number of symbols', 'List symbols', 'List expressions', 
                                 'Add a symbol', 'Add an expression', 'Remove a term', 'Does it contain?', 
                                 'Open a grammar text file', 'Save grammar to a text file', 'Exit'], 
                                 numbered=True)

        match choice:
            case 'Generate a symbol':
                if 0 == len(gb.langMap.keys()): 
                    print("Cannot generate a big nothing symbol!")
                    continue
                choice = pyip.inputMenu(list(gb.langMap.keys()), prompt="Which symbol would you like to generate? Press ENTER to exit\n", numbered=True, blank=True)
                print(gb.generate(choice))
            case 'Generate a number of symbols':
                if 0 == len(gb.langMap.keys()):
                    print("Cannot generate multiple big nothing symbols!")
                    continue
                symbol = pyip.inputMenu(list(gb.langMap.keys()), prompt="Which symbol would you like to generate? Press ENTER to exit\n", numbered=True, blank=True)
                if symbol: 
                    print(f"How many {symbol}'s would you like to print?")
                    symbols = pyip.inputNum(greaterThan=-1)
                    for i in range(symbols):
                        print(f"{i+1}: {gb.generate(symbol)}")
            case 'List symbols':
                for i in gb.langMap.keys():
                    print(i)
            case 'List expressions':
                if 0 == len(gb.langMap.keys()):
                    print("Cannot print a list of big nothing burgers!")
                    continue
                symbol = pyip.inputMenu(list(gb.langMap.keys()), prompt="Which expressions would you like to list? Press ENTER to exit\n", numbered=True, blank=True)
                if symbol and len(gb.langMap[symbol]) > 0:
                    for i in range(len(gb.langMap[symbol])):
                        print(f'{i+1}: {gb.langMap[symbol][i]}')
                else:
                    print("Symbol has no definitions!")        
            case 'Add a symbol':
            #TODO: enter exit
                symbol = input("What symbol would you like to add?\n")
                gb.addSymbol(symbol)
            case 'Add an expression':
            #TODO: enter exit
                symbol = input("What symbol does this expression define?\n")
                expression = input("What is the expression?\n")
                gb.addExpression(symbol=symbol, expression=expression)
            case 'Remove a term':
                choice = pyip.inputMenu(['Symbol', 'Expression'], prompt="Would you like to remove a symbol or an expression? Press ENTER to exit\n", numbered=True, blank=True)
                match choice:
                    case 'Symbol':
                        for i in gb.langMap.keys():
                            print(i)
                        symbol = input("What symbol would you like to remove? Press ENTER to exit\n")
                        if symbol and symbol in gb.langMap.keys():
                            del gb.langMap[symbol]
                        elif symbol and symbol not in gb.langMap.keys():
                            print("Symbol not in grammar!")
                    case 'Expression':
                        if len(gb.langMap.keys()) == 0:
                            print("Cannot remove anything from a big nothing burger!")
                            continue
                        symbol = pyip.inputMenu(list(gb.langMap.keys()), prompt="What symbol is the expression you want to remove? Press ENTER to exit \n", numbered=True, blank=True)
                        if not symbol:
                            continue
                        expression = input("What expression would you like to remove? Press ENTER to exit\n")                        
                        if not expression:
                            continue
                        elif expression in gb.langMap[symbol]:
                            gb.langMap[symbol].remove(expression)
                            print(f'Expression {expression} removed from grammar!')
                    case _:
                        continue
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
