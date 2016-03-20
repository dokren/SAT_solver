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

    maxOccurLiteral = literals.index(max(literals))
    newLiterals = array('i', literals)
    newFormula = deepcopy(formula)
    newFormula.append(array('i', [maxOccurLiteral]))
    (solution, satisfiable) = dpll(newFormula, newLiterals, occurrences)
    if satisfiable:
        return solution, satisfiable
    newLiterals = literals.index(max(literals))
    newFormula = deepcopy(formula)
    newFormula.append(array('i', [-maxOccurLiteral]))
    return dpll(newFormula, newLiterals, occurrences)


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

solve('dimacs/test_case_not_satisfiable.cnf', 'temp/bf0432-007_lol_izi.cnf')
