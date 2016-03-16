from boolean import *

def parseInput(file):
    file = open(file, 'r')
    formula = list()
    literals = dict()
    nbvar = 0
    nbclauses = 0
    for line in file:
        line = line.strip()
        if line.startswith('c'):
            continue
        if line.startswith('p cnf'):
            split = line.split(' ')
            if len(split) != 4:
                raise Exception('File is not in dimacs format!')
            nbvar = int(split[2])
            nbclauses = int(split[3])
            for i in range(1, nbvar+1):
                literals[i] = None
        else:
            if nbclauses == 0 or not line.endswith('0'):
                raise Exception('File is not in dimacs format!')
            clause = Or(map(checkNot, line.split(' ')[:-1]))
            formula.append(clause)
            nbclauses-=1
    return And(formula)
    

def checkNot(x):
    if x.startswith('-'):
        return Not(x[1:])
    return x
