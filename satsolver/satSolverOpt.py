from satParserOpt import *
from copy import deepcopy
import sys


def solve(inputFile, outputFile):
    print('Parsing input file...')
    (formula, literals, occurrences, purity) = parseInput(inputFile)
    print('Removing pure literals...')
    removePureLiterals(formula, literals, occurrences, purity)
    print('Running main DPLL algorithm...')
    (solution, satisfiable) = dpll(formula, literals, occurrences)
    print('Found solution, writing on output file...')
    writeOutput(outputFile, solution, satisfiable)

def removePureLiterals(formula, literals, occurrences, purity):
    for i in range(0, len(occurrences)):
        pure = purity[i]
        if occurrences[i] == abs(pure):
            literals[i] = int(pure/abs(pure))
            formula.append(array('i', [literals[i] * i]))

def dpll(formula, literals, occurrences):
    clearUnits(formula, literals)
    if not formula:
        return literals, True
    elif array('i') in formula:
        return literals, False

    level = 0
    levels = dict()
    i = literals.index(0)
    levels[level] = list([formula, literals, i+1])
    while True:
        print('LEVEL ' + str(level))
        print ('[', end="")
        for (k, v) in levels.items():
            print(str(v[2]) + ",", end="")
        print (']')
        (cFormula, cLiterals, cLit) = levels[level]
        
        newLiterals = array('i', cLiterals)
        newFormula = deepcopy(cFormula)
        if cLit > 0:
            newFormula.append(array('i', [cLit]))
        else:
            newFormula.append(array('i', [-cLit]))
            
        clearUnits(newFormula, newLiterals)
        if not newFormula:
            return literals, True
        elif array('i') in newFormula:
            if cLit > 0:
                levels[level] = list([cFormula, cLiterals, -cLit])
            else:
                if level == 0:
                    return literals, False
                else:
                    level -= 1
                    while levels[level][2] < 0:
                        level -= 1
                    levels[level][2] = -levels[level][2]
        else:
            level += 1
            i = newLiterals.index(0)
            levels[level] = list([newFormula, newLiterals, i+1])


def clearUnits(formula, literals):
    i = 0
    while i < len(formula):
        clause = formula[i]
        if len(clause) == 1:
            literals[abs(clause[0]) - 1] = 1 if clause[0] > 0 else -1
            j = 0
            while j < len(formula):
                next = False
                tempClause = formula[j]
                if set(tempClause) == set(clause):
                    formula.remove(tempClause)
                    next = True
                elif clause[0] in tempClause:
                    formula.remove(tempClause)
                    next = True
                elif -clause[0] in tempClause:
                    tempClause.remove(-clause[0])
                    next = True
                j = j if next else j + 1
            i = 0
            continue
        i += 1

solve('dimacs/sudoku2.txt', 'temp/test2_sol.txt')
