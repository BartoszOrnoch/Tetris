a = [[0, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 1], [1, 1, 1, 1], [0, 1, 0, 1]]


def collapse_array(a):
    rows_removed = 0
    for index, row in enumerate(a[1:], 1):
        if row == [1, 1, 1, 1]:
            a[1:index+1] = a[:index]
            rows_removed += 1

    return rows_removed


print(all([0, 1, 1, 1]))
