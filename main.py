from tkinter import *

import time

start_time = time.time()


def potentialCandidate(x, y):
	candidates = {1, 2, 3, 4, 5, 6, 7, 8, 9}

	global sudoku
	global duSudoku

	for k in range(9):
		if sudoku[x][k] in candidates:
			candidates.remove(sudoku[x][k])
		if sudoku[k][y] in candidates:
			candidates.remove(sudoku[k][y])

	for m in range(x // 3 * 3, x // 3 * 3 + 3):
		for n in range(y // 3 * 3, y // 3 * 3 + 3):
			if sudoku[m][n] in candidates:
				candidates.remove(sudoku[m][n])

	return candidates


def removeUnneeded(x, y):
	global sudoku
	global duSudoku

	for u in range(9):
		if sudoku[x][y] in duSudoku[x][u]:
			duSudoku[x][u].remove(sudoku[x][y])
		if sudoku[x][y] in duSudoku[u][y]:
			duSudoku[u][y].remove(sudoku[x][y])

	for u in range(x // 3 * 3, x // 3 * 3 + 3):
		for p in range(y // 3 * 3, y // 3 * 3 + 3):
			if sudoku[x][y] in duSudoku[u][p]:
				duSudoku[u][p].remove(sudoku[x][y])


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

duSudoku = [[set(), set(), set(), set(), set(), set(), set(), set(), set()],
            [set(), set(), set(), set(), set(), set(), set(), set(), set()],
            [set(), set(), set(), set(), set(), set(), set(), set(), set()],
            [set(), set(), set(), set(), set(), set(), set(), set(), set()],
            [set(), set(), set(), set(), set(), set(), set(), set(), set()],
            [set(), set(), set(), set(), set(), set(), set(), set(), set()],
            [set(), set(), set(), set(), set(), set(), set(), set(), set()],
            [set(), set(), set(), set(), set(), set(), set(), set(), set()],
            [set(), set(), set(), set(), set(), set(), set(), set(), set()],
            ]

root = Tk()

for i in range(9):
	for j in range(9):
		if sudoku[i][j] == 0:
			duSudoku[i][j] = potentialCandidate(i, j)

unchanged = 1
while unchanged:
	unchanged = 0
	for i in range(9):
		for j in range(9):
			if sudoku[i][j] == 0:
				potentialX = set(duSudoku[i][j])
				potentialY = set(duSudoku[i][j])
				potentialCell = set(duSudoku[i][j])

				for m in range(9):
					if m != j:
						potentialX = potentialX.difference(duSudoku[i][m])
					if m != i:
						potentialY = potentialY.difference(duSudoku[m][j])

				for q in range(i // 3 * 3, i // 3 * 3 + 3):
					for r in range(j // 3 * 3, j // 3 * 3 + 3):
						if q != i or r != j:
							potentialCell = potentialCell.difference(duSudoku[q][r])
				potentialX = potentialX.union(potentialY.union(potentialCell))

				if len(potentialX) == 1:
					sudoku[i][j] = potentialX.pop()
					removeUnneeded(i, j)
					duSudoku[i][j].clear()
					unchanged = 1
					break

				count = 0
				for k in range(9):
					if k >= i and duSudoku[i][j] == duSudoku[i][k]:
						count += 1
						if count == len(duSudoku[i][j]):
							unchanged = 1
							for m in range(9):
								if duSudoku[i][m] != duSudoku[i][j]:
									duSudoku[i][m] = duSudoku[i][m].difference(duSudoku[i][j])

				count = 0
				for k in range(9):
					if k >= j and duSudoku[i][j] == duSudoku[k][j]:
						count += 1
						if count == len(duSudoku[i][j]):
							unchanged = 1
							for m in range(9):
								if duSudoku[m][j] != duSudoku[i][j]:
									duSudoku[m][j] = duSudoku[m][j].difference(duSudoku[i][j])

				count = 0
				for k in range(i // 3 * 3, i // 3 * 3 + 3):
					for q in range(j // 3 * 3, j // 3 * 3 + 3):
						if duSudoku[i][j] == duSudoku[k][q]:
							count += 1
							if count == len(duSudoku[i][j]):
								unchanged = 1
								for m in range(i // 3 * 3, i // 3 * 3 + 3):
									for n in range(j // 3 * 3, j // 3 * 3 + 3):
										if duSudoku[m][n] != duSudoku[i][j]:
											duSudoku[m][n] = duSudoku[m][n].difference(duSudoku[i][j])

for t in sudoku:
	print(t)