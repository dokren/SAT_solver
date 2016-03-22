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
            occurrences[i] += 1
            formula.append(list([i+1]))

def dpll(formula, literals, occurrences):

    (formula, literals, occurrences) = clearUnits(formula, literals, occurrences)

    if not formula:
        return literals, True
    elif [] in formula:
        return literals, False

    level = 0
    levels = dict()
    i = occurrences.index(max(occurrences))

    levels[level] = list([formula, literals, i+1, occurrences])
    while True:
        (cFormula, cLiterals, cLit, cOcc) = levels[level]

        newLiterals = list(cLiterals)
        newFormula = deepcopy(cFormula)
        newOcc = list(cOcc)

        newFormula.append([cLit])

        (newFormula, newLiterals, newOcc) = clearUnits(newFormula, newLiterals, newOcc)

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
                        if level == 0:
                            return newLiterals, False
                        level -= 1
                    levels[level][2] = -levels[level][2]
        else:
            level += 1
            i = newOcc.index(max(newOcc))
            levels[level] = list([newFormula, newLiterals, i+1, newOcc])


def clearUnits(formula, literals, occurrences):

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
        newOcc = array('i', (0,)*len(occurrences))
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
                for i in newClause:
                    newOcc[abs(i) - 1] += 1
                newFormula.append(newClause)

        formula = newFormula
        occurrences = newOcc
    return (formula, literals, occurrences)


# solve('dimacs/test2.txt', 'temp/test2_sol.txt')
solve('dimacs/test_case_not_satisfiable.cnf', 'temp/test_case_not_satisfiable.cnf_sol.cnf')
