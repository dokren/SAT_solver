from satParser import *
from copy import deepcopy


def solve(inputFile, outputFile):
    (formula, literals) = parseInput(inputFile)
    print('FORMULA: ' + str(formula))
    print('LITERALS: ' + str(literals))

    (solution, satisfiable) = dpll(formula, literals)

    print('IS SATISFIABLE: ' + str(satisfiable))
    print('END SOLUTION: ' + str(solution))

    writeOutput(outputFile, solution, satisfiable)


def dpll(formula, literals):
    clearUnits(formula, literals)
    if not formula:
        return literals, True
    elif [] in formula:
        return literals, False

    for (k, v) in literals.items():
        if v == None:
            newLiterals = dict(literals)
            newFormula = deepcopy(formula)
            newFormula.append([k])
            (solution, satisfiable) = dpll(newFormula, newLiterals)
            if satisfiable:
                return solution, satisfiable
            newLiterals = dict(literals)
            newFormula = deepcopy(formula)
            newFormula.append([-k])
            return dpll(newFormula, newLiterals)


def clearUnits(formula, literals):
    i = 0
    while i < len(formula):
        clause = formula[i]
        if len(clause) == 1:
            literals[abs(clause[0])] = True if clause[0] > 0 else False
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


solve('dimacs/sudoku2.txt', 'temp/sudoku2_lol_izi.txt')
