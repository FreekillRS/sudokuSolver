# Sudoku Solver
My solution to the Sudoku game.

It finds all possible numbers for each empty slot and narrows them down until a single number remains, more messy but overall faster than backtracking.
**GUI** was made in **TKinter**.

**Step-By-Step** option shows some parts of the process, you can ajust the speed it is going by changing the `timer` value.
Yellow tiles indicate a try to exclude values based on the values that are already found.
Purple tiles indicate a try to pinpoint a value that can only be in that spot based on values which can't be in any other spot in its block, row or column.

An example matrix automatically loads on start if you want to test it out.
