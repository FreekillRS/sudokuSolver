# Sudoku Solver
Sudoku with Step-By-Step solver and TKinter GUI.

Finds all possible numbers for each empty slot and narrows them down until a single number remains, more messy but overall faster than backtracking.

**Step-By-Step** option shows parts of the process, you can adjust the speed it is going by changing the `timer` value.
Yellow tiles indicate a try to exclude values based on the values that are already found.
Purple tiles indicate a try to pinpoint a value that can only be in that spot based on values which can't be in any other spot in its block, row or column.

An example matrix automatically loads on start.
