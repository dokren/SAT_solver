from boolean import *
from satParser import *

def solve(file):
    (formula, literals) = parseInput(file)
    print('FORMULA: ' + str(formula))
    print(dpll(formula, literals))
    

def dpll(formula, literals):
    print('FORMULA:')
    print(formula)
    formula = formula.simplify()
    print('FORMULA - SIMPLIFIED:')
    print(formula)
    if formula == T:
        return literals
    if formula == F:
        return None
    if isinstance(formula, Literal):
        literals[formula.lit] = True
        return literals
    if isinstance(formula, Not):
        literals[formula.term.lit] = False
        return literals
    if isinstance(formula, Or):
        item = next(iter(formula.lst))
        if isinstance(item, Literal):
            literals[item.lit] = True
            return literals
        if isinstance(item, Not):
            literals[item.term.lit] = False
            return literals
    ## remove unit clauses and set them the required value
    for clause in formula.lst:
        if isinstance(clause, Literal):
            literals[clause.lit] = True
            formula = formula.removeClause(clause)
        if isinstance(clause, Not):
            literals[clause.term.lit] = False
            formula = formula.removeClause(clause)

    if formula == T:
        return literals
    if formula == F:
        return None
    
    
    for (k,v) in literals.items():
        if v == None:
            newLiterals = dpll(formula.addClause(Literal(k)), dict(literals))
            if not newLiterals is None:
                return newLiterals
            else:
                return dpll(formula.addClause(Not(Literal(k))), dict(literals))
    
solve('dimacs/test.txt')
