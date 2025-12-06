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
import random

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
            print("Rule set cannot be empty")
            return
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
        with open(filename, 'w') as file:
            for k in self.langMap.keys():
                line = k + self.symDelim
                for v in self.langMap[k]:
                    if v == self.langMap[k][-1]:
                        line += v
                    else:    
                        line += v + self.exprDelim
                file.write(line + '\n')
        file.close()         

    #TODO: updateMap func for updating existing langMap with supplied rule set, empty ruleset may cause a null map to exist after calling constructor