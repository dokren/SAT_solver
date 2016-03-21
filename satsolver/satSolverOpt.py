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
            formula.append(list([literals[i]]))

def dpll(formula, literals, occurrences):
    (formula, literals) = clearUnits(formula, literals)
    if not formula:
        return literals, True
    elif [] in formula:
        return literals, False

    level = 0
    levels = dict()
    i = literals.index(0)
    levels[level] = list([formula, literals, i+1])
    while True:
        (cFormula, cLiterals, cLit) = levels[level]

        newLiterals = list(cLiterals)
        newFormula = deepcopy(cFormula)
        print(newLiterals)

        newFormula.append([cLit])

        (newFormula, newLiterals) = clearUnits(newFormula, newLiterals)


        if not newFormula:
            return newLiterals, True
        elif [] in newFormula:
            if cLit > 0:
                levels[level][2] = -cLit
            else:
                if level == 0:
                    return newLiterals, False
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

    loop = True
    while loop:
        loop = False
        units = list()
        for clause in formula:
            if len(clause) == 1 and not -clause[0] in units:
                loop = True
                literals[abs(clause[0]) - 1] = 1 if clause[0] > 0 else -1
                units.append(clause[0])

        negativeUnits = list(map(lambda x: x * -1, units))

        newFormula = list()
        for clause in formula:
            if len(clause) == 1 and clause[0] in units:
                continue
            newClause = list()
            add = True
            for lit in clause:
                if lit in units:
                    add = False
                if lit in negativeUnits:
                    continue
                newClause.append(lit)
            if add:
                newFormula.append(newClause)

        formula = newFormula
    return (formula, literals)


# solve('dimacs/test2.txt', 'temp/test2_sol.txt')
solve('dimacs/test_case_not_satisfiable.cnf', 'temp/test_case_satisfiable_sol.cnf')
