a = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [
    0, 0, 1, 1, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0]]


def rotate(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows-1, -1, -1):
        matrix[i].reverse()
        for j in range(cols):
            if i == j:
                a = matrix[i].pop()
                continue
            matrix[j].append(matrix[i].pop())
        matrix[i].reverse()
        matrix[i].append(a)
    return matrix


print(rotate(rotate(rotate(a))))
