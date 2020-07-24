import time
from tkinter import *


def clear(everything):
	for i in range(9):
		for j in range(9):
			if changed[i][j] or everything:
				sudoku[i][j] = 0
				table[i][j].config(text=str(sudoku[i][j]))
	root.update()


def buttonClick(stepByStep):
	for i in range(9):
		for j in range(9):
			try:
				sudoku[i][j] = int(table[i][j].get())
			except ValueError:
				sudoku[i][j] = 0

	for i in range(9):
		for j in range(9):
			if sudoku[i][j] == 0:
				duSudoku[i][j] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

				for k in range(9):
					if sudoku[i][k] in duSudoku[i][j]:
						duSudoku[i][j].remove(sudoku[i][k])
					if sudoku[k][j] in duSudoku[i][j]:
						duSudoku[i][j].remove(sudoku[k][j])

				for m in range(i // 3 * 3, i // 3 * 3 + 3):
					for n in range(j // 3 * 3, j // 3 * 3 + 3):
						if sudoku[m][n] in duSudoku[i][j]:
							duSudoku[i][j].remove(sudoku[m][n])
			else:
				table[i][j].insert(0, sudoku[i][j])
				table[i][j].config(fg="black")

	timer = 0.05
	change = 1
	while change:
		change = 0
		for i in range(9):
			for j in range(9):
				if sudoku[i][j] == 0:
					color = table[i][j].cget("bg")
					table[i][j].config(bg="red")
					if stepByStep:
						root.update()

					potentialX = set(duSudoku[i][j])
					potentialY = set(duSudoku[i][j])
					potentialCell = set(duSudoku[i][j])

					for m in range(9):
						color1 = table[i][m].cget("bg")
						color2 = table[m][j].cget("bg")
						if m != j:
							potentialX = potentialX.difference(duSudoku[i][m])

							table[i][m].config(bg="yellow")
						if m != i:
							potentialY = potentialY.difference(duSudoku[m][j])

							table[m][j].config(bg="yellow")

						if stepByStep:
							root.update()
							time.sleep(timer)

						table[i][m].config(bg=color1)
						table[m][j].config(bg=color2)

					for q in range(i // 3 * 3, i // 3 * 3 + 3):
						for r in range(j // 3 * 3, j // 3 * 3 + 3):
							if q != i or r != j:
								potentialCell = potentialCell.difference(duSudoku[q][r])
								color1 = table[q][r].cget("bg")
								table[q][r].config(bg="yellow")

								if stepByStep:
									root.update()
									time.sleep(timer)

								table[q][r].config(bg=color1)

					potentialX = potentialX.union(potentialY.union(potentialCell))

					if len(potentialX) == 1:
						color1 = table[i][j].cget("bg")
						sudoku[i][j] = potentialX.pop()

						table[i][j].delete(0, END)
						table[i][j].insert(0, sudoku[i][j])
						table[i][j].config(bg="green")

						if stepByStep:
							root.update()
							time.sleep(timer * 3)

						table[i][j].config(bg=color1)

						removeUnneeded(i, j)
						duSudoku[i][j].clear()
						change = 1
						table[i][j].config(bg=color)
						continue

					count = 1
					for k in range(9):
						if k > j:
							color1 = table[i][k].cget("bg")
							table[i][k].config(bg="purple")

							if stepByStep:
								root.update()
								time.sleep(timer)

							table[i][k].config(bg=color1)

							if duSudoku[i][j] == duSudoku[i][k]:
								count += 1
								if count == len(duSudoku[i][j]):
									change = 1
									for m in range(9):
										if duSudoku[i][m] != duSudoku[i][j]:
											duSudoku[i][m] = duSudoku[i][m].difference(duSudoku[i][j])

					count = 1
					for k in range(9):
						if k > i:
							color1 = table[k][j].cget("bg")
							table[k][j].config(bg="purple")

							if stepByStep:
								root.update()
								time.sleep(timer)

							table[k][j].config(bg=color1)

							if duSudoku[i][j] == duSudoku[k][j]:
								count += 1
								if count == len(duSudoku[i][j]):
									change = 1
									for m in range(9):
										if duSudoku[m][j] != duSudoku[i][j]:
											duSudoku[m][j] = duSudoku[m][j].difference(duSudoku[i][j])

					count = 0
					for k in range(i // 3 * 3, i // 3 * 3 + 3):
						for q in range(j // 3 * 3, j // 3 * 3 + 3):
							if duSudoku[i][j] == duSudoku[k][q]:
								count += 1
								if count == len(duSudoku[i][j]):
									change = 1
									for m in range(i // 3 * 3, i // 3 * 3 + 3):
										for n in range(j // 3 * 3, j // 3 * 3 + 3):
											if duSudoku[m][n] != duSudoku[i][j]:
												duSudoku[m][n] = duSudoku[m][n].difference(duSudoku[i][j])
					table[i][j].config(bg=color)


def removeUnneeded(x, y):
	for u in range(9):
		if sudoku[x][y] in duSudoku[x][u]:
			duSudoku[x][u].remove(sudoku[x][y])
		if sudoku[x][y] in duSudoku[u][y]:
			duSudoku[u][y].remove(sudoku[x][y])

	for u in range(x // 3 * 3, x // 3 * 3 + 3):
		for p in range(y // 3 * 3, y // 3 * 3 + 3):
			if sudoku[x][y] in duSudoku[u][p]:
				duSudoku[u][p].remove(sudoku[x][y])


root = Tk()
root.title("Sudoku Solver")
root.iconbitmap('sudoku.ico')
root.resizable(False, False)

sudoku = [[0, 0, 0, 8, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 4, 3],
          [5, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 7, 0, 8, 0, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0],
          [0, 2, 0, 0, 3, 0, 0, 0, 0],
          [6, 0, 0, 0, 0, 0, 0, 7, 5],
          [0, 0, 3, 4, 0, 0, 0, 0, 0],
          [0, 0, 0, 2, 0, 0, 6, 0, 0]
          ]

# sudoku = []
duSudoku = []
changed = []
table = []

for row in range(9):
	table += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
	duSudoku += [[set(), set(), set(), set(), set(), set(), set(), set(), set()]]

	for column in range(9):
		table[row][column] = Entry(root, width=2, justify="center", relief="solid", font="Helvetica 18")
		table[row][column].grid(row=row, column=column)

		if ((row < 3 or row > 5) and (column < 3 or column > 5)) or (2 < row < 6 and 2 < column < 6):
			table[row][column].config(bg="#a3a3a3")
		else:
			table[row][column].config(bg="#d4d4d4")

solveFastButton = Button(root, text="Solve", width=15, relief="flat", command=lambda: buttonClick(0))
solveStepButton = Button(root, text="Step-By-Step", width=20, relief="flat", command=lambda: buttonClick(1))
resetButton = Button(root, text="Reset", width=15, relief="flat", command=lambda: buttonClick(1))
clearButton = Button(root, text="Clear Result", width=20, relief="flat", command=lambda: buttonClick(0))
infoText = Label(root, text="Enter the puzzle then click Solve or Step-By-Step!", justify="center", fg="blue")

solveFastButton.grid(row=9, column=0, columnspan=4)
solveStepButton.grid(row=9, column=4, columnspan=5)
resetButton.grid(row=10, column=0, columnspan=4)
clearButton.grid(row=10, column=4, columnspan=5)
infoText.grid(row=11, column=0, columnspan=9)

root.mainloop()
