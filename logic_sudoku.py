import numpy as np

unsolved = np.array(np.matrix('1 0 4 0 0 6 9 8 2; 2 0 0 9 0 0 0 0 0 ; 0 3 0 0 0 0 1 0 4; 0 0 5 0 8 2 6 0 0 ; 6 0 9 0 1 0 5 0 8 ; 0 0 3 6 9 0 2 0 0 ; 3 0 8 0 0 0 0 2 0 ; 0 0 0 0 0 4 0 0 1; 4 6 1 5 0 0 8 0 9'))
#unsolved = np.array(np.matrix('5 3 0 0 7 0 0 0 0 ; 6 0 0 1 9 5 0 0 0 ; 0 9 8 0 0 0 0 6 0 ; 8 0 0 0 6 0 0 0 3; 4 0 0 8 0 3 0 0 1; 7 0 0 0 2 0 0 0 6 ; 0 6 0 0 0 0 2 8 0 ; 0 0 0 4 1 9 0 0 5; 0 0 0 0 8 0 0 7 9'))
#unsolved = np.array(np.matrix('8 7 6 9 0 0 0 0 0 ; 0 1 0 0 0 6 0 0 0 ; 0 4 0 3 0 5 8 0 0 ; 4 0 0 0 0 0 2 1 0 ; 0 9 0 5 0 0 0 0 0 ; 0 5 0 0 4 0 3 0 6 ; 0 2 9 0 0 0 0 0 8 ; 0 0 4 6 9 0 1 7 3 ; 0 0 0 0 0 1 0 0 4'))
possibles = [[list(range(1,10)) for i in range(9)] for j in range(9)]

for row in range(9):
    for col in range(9):
        if unsolved[row][col] != 0:
            possibles[row][col] = unsolved[row][col]

i, j = np.where(unsolved == 0)
allZeros = list(map(list, list(zip(i, j))))

# eliminate from possible values if it's in the row or the column
for coord in allZeros:
    row = coord[0]
    col = coord[1]
    thisRow = np.delete(unsolved[row,:], col)
    thisCol = np.delete(unsolved[:,col], row)
    thisPossibles = possibles[row][col]
    for value in thisRow:
        thisPossibles = np.delete(thisPossibles, np.where(thisPossibles == value))
    for value in thisCol:
        thisPossibles = np.delete(thisPossibles, np.where(thisPossibles == value))
    possibles[row][col] = thisPossibles

# eliminate from possible values if it's in the same 3x3 grid
for coord in allZeros:
    row = coord[0]
    col = coord[1]
    thisPossibles = possibles[row][col]
    thisChunk = unsolved[row//3*3:row//3*3+3, col//3*3:col//3*3+3]
    for value in thisChunk:
        thisPossibles = np.delete(thisPossibles, np.where(thisPossibles == value))
    possibles[row][col] = thisPossibles

# fill in the boxes that are known and update zeros
for coord in allZeros:
    row = coord[0]
    col = coord[1]
    if len(possibles[row][col]) == 1:
        unsolved[row][col] = possibles[row][col][0]
    i, j = np.where(unsolved == 0)
    allZeros = list(map(list, list(zip(i, j))))


for row in range(9):
    rowZeros = [i for i in possibles[row] if type(i) == np.ndarray]
    flatRowZeros = [i for j in rowZeros for i in j]
    uniqueFlatRowZeros = [i for i in flatRowZeros if flatRowZeros.count(i) == 1]
    if len(uniqueFlatRowZeros) == 1:
        rowWeKnow = [i.tolist() if type(i) == np.ndarray else i for i in possibles[row]]
        rowWeKnow = [[i] if type(i) != list else i for i in rowWeKnow]
        indexWeWant = [1 if uniqueFlatRowZeros[0] in i else 0 for i in rowWeKnow].index(1)
        possibles[row][indexWeWant] = uniqueFlatRowZeros

possibles = list(map(list, list(zip(*possibles))))

for row in range(9):
    rowZeros = [i for i in possibles[row] if type(i) == np.ndarray]
    flatRowZeros = [i for j in rowZeros for i in j]
    uniqueFlatRowZeros = [i for i in flatRowZeros if flatRowZeros.count(i) == 1]
    if len(uniqueFlatRowZeros) == 1:
        rowWeKnow = [i.tolist() if type(i) == np.ndarray else i for i in possibles[row]]
        rowWeKnow = [[i] if type(i) != list else i for i in rowWeKnow]
        indexWeWant = [1 if uniqueFlatRowZeros[0] in i else 0 for i in rowWeKnow].index(1)
        possibles[row][indexWeWant] = uniqueFlatRowZeros

possibles = list(map(list, list(zip(*possibles))))


for coord in allZeros:
    row = coord[0]
    col = coord[1]
    if len(possibles[row][col]) == 1:
        unsolved[row][col] = possibles[row][col][0]
    i, j = np.where(unsolved == 0)
    allZeros = list(map(list, list(zip(i, j))))

# still need to get rid of loners in chunks
# ie if a value can only be in one spot in a chunk, then fill it in
