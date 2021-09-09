import time
from tkinter import *


def updateColor(stepByStep, wait):
	if stepByStep:
		root.update()
		time.sleep(wait)


def noSolution(check, i, j, color=None):
	if check == set():
		infoText['text'] = "This puzzle doesn't have a solution!"
		clearButton['state'] = NORMAL
		resetButton['state'] = NORMAL
		if color:
			table[i][j]['bg'] = color
		else:
			solveStepButton['state'] = NORMAL
			solveFastButton['state'] = NORMAL
		return 1


def insertNumber(i, j, stepByStep, timer):
	color1 = table[i][j].cget('bg')

	table[i][j].delete(0, END)
	table[i][j].insert(0, next(iter(duSudoku[i][j])))
	changed[i][j] = 2
	table[i][j]['bg'] = 'green'

	if stepByStep:
		root.update()
		time.sleep(timer * 5)

	table[i][j]['bg'] = color1

	for u in range(9):
		if u != j:
			duSudoku[i][u] = duSudoku[i][u].difference(duSudoku[i][j])
		if u != i:
			duSudoku[u][j] = duSudoku[u][j].difference(duSudoku[i][j])

	for u in range(i // 3 * 3, i // 3 * 3 + 3):
		for p in range(j // 3 * 3, j // 3 * 3 + 3):
			if u != i or p != j:
				duSudoku[u][p] = duSudoku[u][p].difference(duSudoku[i][j])

	return 1


def clear(everything):
	for i in range(9):
		for j in range(9):
			if changed[i][j] or everything:
				duSudoku[i][j] = 0
				table[i][j].delete(0, END)
				table[i][j]['fg'] = 'black'
	infoText['text'] = 'Enter the puzzle then click Solve or Step-By-Step!'
	solveStepButton['state'] = NORMAL
	solveFastButton['state'] = NORMAL
	root.update()


def buttonClick(stepByStep):
	infoText['text'] = 'Solving...'
	start = time.time()
	solveStepButton['state'] = DISABLED
	solveFastButton['state'] = DISABLED
	clearButton['state'] = DISABLED
	resetButton['state'] = DISABLED
	root.update()

	for i in range(9):
		for j in range(9):
			try:
				duSudoku[i][j] = {int(table[i][j].get())}
				changed[i][j] = 0
				table[i][j]['fg'] = 'black'
			except ValueError:
				duSudoku[i][j] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
				changed[i][j] = 1
				table[i][j]['fg'] = 'red'

	for i in range(9):
		for j in range(9):
			if len(duSudoku[i][j]) > 1:
				for k in range(9):
					if len(duSudoku[i][k]) == 1:
						duSudoku[i][j] = duSudoku[i][j].difference(duSudoku[i][k])

					if len(duSudoku[k][j]) == 1:
						duSudoku[i][j] = duSudoku[i][j].difference(duSudoku[k][j])

				for m in range(i // 3 * 3, i // 3 * 3 + 3):
					for n in range(j // 3 * 3, j // 3 * 3 + 3):
						if len(duSudoku[m][n]) == 1:
							duSudoku[i][j] = duSudoku[i][j].difference(duSudoku[m][n])
			else:
				for k in range(9):
					if (k != j and duSudoku[i][j] == duSudoku[i][k]) or (k != i and duSudoku[i][j] == duSudoku[k][j]):
						noSolution(set(), i, j)
						return

				for m in range(i // 3 * 3, i // 3 * 3 + 3):
					for n in range(j // 3 * 3, j // 3 * 3 + 3):
						if duSudoku[i][j] == duSudoku[m][n] and (i != m or j != n):
							noSolution(set(), i, j)
							return

	timer = 0.005
	change = 1

	while change:
		change = 0

		for i in range(9):
			for j in range(9):
				color = table[i][j].cget('bg')

				if len(duSudoku[i][j]) > 1:
					color = table[i][j].cget('bg')
					table[i][j]['bg'] = 'red'

					if stepByStep:
						root.update()

					potentialX = set(duSudoku[i][j])
					potentialY = set(duSudoku[i][j])
					potentialCell = set(duSudoku[i][j])

					for m in range(9):
						color1 = table[i][m].cget('bg')
						color2 = table[m][j].cget('bg')

						if m != j:
							potentialX = potentialX.difference(duSudoku[i][m])
							table[i][m]['bg'] = 'yellow'

						if m != i:
							potentialY = potentialY.difference(duSudoku[m][j])
							table[m][j]['bg'] = 'yellow'

						updateColor(stepByStep, timer)

						table[i][m]['bg'] = color1
						table[m][j]['bg'] = color2

					for q in range(i // 3 * 3, i // 3 * 3 + 3):
						for r in range(j // 3 * 3, j // 3 * 3 + 3):
							if q != i or r != j:
								potentialCell = potentialCell.difference(duSudoku[q][r])
								color1 = table[q][r].cget('bg')
								table[q][r]['bg'] = 'yellow'

								updateColor(stepByStep, timer)

								table[q][r]['bg'] = color1

					potentialX = potentialX.union(potentialY.union(potentialCell))

					if len(potentialX) == 1:
						duSudoku[i][j] = potentialX

						change = insertNumber(i, j, stepByStep, timer)

						table[i][j]['bg'] = color
						continue

					count = 1
					for k in range(j + 1, 9):
						color1 = table[i][k].cget('bg')
						table[i][k]['bg'] = 'purple'

						updateColor(stepByStep, timer)

						table[i][k]['bg'] = color1
						if duSudoku[i][j] == duSudoku[i][k]:
							count += 1

							if count == len(duSudoku[i][j]):
								for m in range(9):
									if duSudoku[i][m] != duSudoku[i][j]:
										duSudoku[i][m] = duSudoku[i][m].difference(duSudoku[i][j])

										if noSolution(duSudoku[i][m], i, j, color):
											return

										change = 1

					count = 1
					for k in range(i + 1, 9):
						color1 = table[k][j].cget('bg')
						table[k][j]['bg'] = 'purple'

						updateColor(stepByStep, timer)

						table[k][j]['bg'] = color1

						if duSudoku[i][j] == duSudoku[k][j]:
							count += 1

							if count == len(duSudoku[i][j]):
								for m in range(9):
									if duSudoku[m][j] != duSudoku[i][j]:
										duSudoku[m][j] = duSudoku[m][j].difference(duSudoku[i][j])

										if noSolution(duSudoku[m][j], i, j, color):
											return

										change = 1

					count = 0
					for k in range(i // 3 * 3, i // 3 * 3 + 3):
						for q in range(j // 3 * 3, j // 3 * 3 + 3):
							color1 = table[k][q].cget('bg')
							table[k][q]['bg'] = 'purple'

							updateColor(stepByStep, timer)

							table[k][q]['bg'] = color1

							if duSudoku[i][j] == duSudoku[k][q]:
								count += 1

								if count == len(duSudoku[i][j]):

									for m in range(i // 3 * 3, i // 3 * 3 + 3):
										for n in range(j // 3 * 3, j // 3 * 3 + 3):
											if duSudoku[m][n] != duSudoku[i][j]:
												duSudoku[m][n] = duSudoku[m][n].difference(duSudoku[i][j])

												if noSolution(duSudoku[m][n], i, j, color):
													return

												change = 1

				elif changed[i][j] == 1 and len(duSudoku[i][j]) == 1:
					change = insertNumber(i, j, stepByStep, timer)
				table[i][j]['bg'] = color

	clearButton['state'] = NORMAL
	resetButton['state'] = NORMAL

	print(str(time.time() - start) + " seconds")

	for i in duSudoku:
		for j in i:
			if len(j) > 1:
				infoText['text'] = "This puzzle doesn't have an unique solution!"
				return

	infoText['text'] = 'Enter the puzzle then click Solve or Step-By-Step!'


root = Tk()
root.title('Sudoku Solver')
root.iconbitmap('sudoku.ico')
root.resizable(False, False)

duSudoku = []
changed = []
table = []

for row in range(9):
	duSudoku += [[set(), set(), set(), set(), set(), set(), set(), set(), set()]]
	changed += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
	table += [[0, 0, 0, 0, 0, 0, 0, 0, 0]]

	for column in range(9):
		table[row][column] = Entry(root, width=2, justify='center', relief='solid', font='Helvetica 18')
		table[row][column].grid(row=row, column=column)

		if ((row < 3 or row > 5) and (column < 3 or column > 5)) or (2 < row < 6 and 2 < column < 6):
			table[row][column]['bg'] = '#a3a3a3'
		else:
			table[row][column]['bg'] = '#d4d4d4'

solveFastButton = Button(root, text='Solve', width=15, relief='flat', command=lambda: buttonClick(0))
solveStepButton = Button(root, text='Step-By-Step', width=20, relief='flat', command=lambda: buttonClick(1))
resetButton = Button(root, text='Reset', width=15, relief='flat', command=lambda: clear(1))
clearButton = Button(root, text='Clear Result', width=20, relief='flat', command=lambda: clear(0))
infoText = Label(root, text='Enter the puzzle then click Solve or Step-By-Step!', justify='center', fg='blue')

solveFastButton.grid(row=9, column=0, columnspan=4)
solveStepButton.grid(row=9, column=4, columnspan=5)
resetButton.grid(row=10, column=0, columnspan=4)
clearButton.grid(row=10, column=4, columnspan=5)
infoText.grid(row=11, column=0, columnspan=9)

table[0][3].insert(0, 8)
table[0][5].insert(0, 1)
table[1][7].insert(0, 4)
table[1][8].insert(0, 3)
table[2][0].insert(0, 5)
table[3][4].insert(0, 7)
table[3][6].insert(0, 8)
table[4][6].insert(0, 1)
table[5][1].insert(0, 2)
table[5][4].insert(0, 3)
table[6][0].insert(0, 6)
table[6][7].insert(0, 7)
table[6][8].insert(0, 5)
table[7][2].insert(0, 3)
table[7][3].insert(0, 4)
table[8][3].insert(0, 2)
table[8][6].insert(0, 6)

root.mainloop()
