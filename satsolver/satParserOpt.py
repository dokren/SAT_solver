from array import array

def parseInput(file):
    file = open(file, 'r')
    formula = list()
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
            # values of literals: -1: false, 0: n/a, 1: true
            literals = array('i', (0,)*nbvar)
            # how many times does a literal occur in formula
            occurrences = array('i', (0,)*nbvar)
            # sums occurrences of a literal i in original formula: +1 for True, -1 for False
            purity = array('i', (0,)*nbvar)
        else:
            try:
                if nbclauses == 0 or not line.endswith('0'):
                    raise Exception('File is not in dimacs format!')
                clause = list(map(int, filter(removeEmpty, line.split()[:-1])))
                for i in clause:
                    occurrences[abs(i)-1] += 1
                    purity[abs(i)-1] += int(i/abs(i))
                formula.append(clause)
                nbclauses -= 1
            except NameError:
                raise Exception('File is not in dimacs format!')
    
    file.close()
    return (formula, literals, occurrences, purity)


def removeEmpty(x):
    if x == '':
        return False
    return True


def writeOutput(file, literals, satisfiable):
    file = open(file, 'w')
    if not satisfiable:
        file.write('NOT SATISFIABLE!')
    else:
        for i in range(1, len(literals)+1):
            if literals[i-1] > 0:
                file.write(str(i) + ' ')
            else:
                file.write('-' + str(i) + ' ')

    file.close()

