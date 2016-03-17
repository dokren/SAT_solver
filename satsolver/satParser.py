def parseInput(file):
    file = open(file, 'r')
    formula = list()
    literals = dict()
    nbclauses = 0
    for line in file:
        line = line.strip()
        if line.startswith('c'):
            continue
        if line.startswith('p cnf'):
            split = line.split()
            if len(split) != 4:
                raise Exception('File is not in dimacs format!')
            nbvar = int(split[2])
            nbclauses = int(split[3])
            for i in range(1, nbvar+1):
                literals[i] = None
        else:
            if nbclauses == 0 or not line.endswith('0'):
                raise Exception('File is not in dimacs format!')
            clause = list(map(int, filter(removeEmpty, line.split()[:-1])))
            formula.append(clause)
            nbclauses -= 1
    file.close()
    return formula, literals


def removeEmpty(x):
    if x == '':
        return False
    return True
