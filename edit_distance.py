import numpy as np


def calc_min_edit_dist(source, target) -> int:
    # Matrix to store the minimum edit distances for dynamic programming
    med_mat = np.zeros((len(source) + 1, len(target) + 1), dtype=int)

    # iterate through substrings, calculate edit distance using dynamic programming
    for r in range(len(source) + 1):
        for c in range(len(target) + 1):
            if r == 0:
                med_mat[r, c] = c
            elif c == 0:
                med_mat[r, c] = r
            elif source[r - 1] == target[c - 1]:
                med_mat[r, c] = med_mat[r - 1, c - 1]
            else:
                med_mat[r, c] = min(
                    med_mat[r - 1, c] + 1,
                    med_mat[r, c - 1] + 1,
                    med_mat[r - 1, c - 1] + 2
                )

    return med_mat[len(source), len(target)]


def align(source, target) -> tuple[list, list, list]:
    med_mat = np.zeros((len(source) + 1, len(target) + 1), dtype=int)
    op_mat = np.zeros((len(source) + 1, len(target) + 1), dtype=object)

    for r in range(len(source) + 1):
        for c in range(len(target) + 1):
            if r == 0:
                med_mat[r, c] = c
                op_mat[r, c] = "i"
            elif c == 0:
                med_mat[r, c] = r
                op_mat[r, c] = "d"
            elif source[r - 1] == target[c - 1]:
                med_mat[r, c] = med_mat[r - 1, c - 1]
                op_mat[r, c] = "x"
            else:
                med_mat[r, c] = min(
                    med_mat[r - 1, c - 1] + 2,
                    med_mat[r - 1, c] + 1,
                    med_mat[r, c - 1] + 1
                )

                if med_mat[r, c] == med_mat[r - 1, c - 1] + 2:
                    op_mat[r, c] = "s"
                elif med_mat[r, c] == med_mat[r - 1, c] + 1:
                    op_mat[r, c] = "d"
                else:
                    op_mat[r, c] = "i"

    op_list = []
    r = len(source)
    c = len(target)
    while r > 0 or c > 0:
        op_list.append(op_mat[r, c])
        if op_mat[r, c] == "x" or op_mat[r, c] == "s":
            r -= 1
            c -= 1
        elif op_mat[r, c] == "i":
            c -= 1
        else:
            r -= 1

    op_list.reverse()
    source = list(source)
    target = list(target)
    for i, op in enumerate(op_list):
        if op == "i":
            source.insert(i, "*")
        if op == "d":
            target.insert(i, "*")

    return source, target, op_list
