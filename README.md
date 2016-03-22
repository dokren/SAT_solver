# SAT solver
A short program that solves the SAT problem using the DPLL algorithm.

## Contents
In subfolder *cases* there are several examples for solving the SAT problem. Two of which solve sudoku for 4×4 and 9×9 instances. Other than these test cases, file in dimacs format is a valid input. It is assumed however, that line starting with "p" comes before all the clauses and that each clause is in it's own line, ending with 0.

## Running the program
The program is ran by executing the program in this way:
```
python satSolverOpt.py [fileName]
```
where fileName is actually path to the file containing valid SAT problem in dimacs format. To access test cases, full command should be e.g.
```
python satSolverOpt.py cases/sudoku1.txt
```
Solution is saved in the same directory with suffix "_sol" attached to the base name of the file.

### Contributors:
Rok Koleša, Domen Kren