import time
import random

from torch import solve

sudoku4 = [[0, 0, 0, 2],
           [2, 4, 0, 3],
           [0, 0, 0, 0],
           [0, 1, 4, 0]]

sudoku9 = [[4, 0, 0, 0, 0, 5, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 1, 9, 8],
           [3, 0, 0, 0, 8, 2, 4, 0, 0],
           [0, 0, 0, 1, 0, 0, 0, 8, 0],
           [9, 0, 3, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 3, 0, 6, 7, 0],
           [0, 5, 0, 0, 0, 9, 0, 0, 0],
           [0, 0, 0, 2, 0, 0, 9, 0, 7],
           [6, 4, 0, 3, 0, 0, 0, 0, 0]]


sudoku = sudoku9


def expand_sudoku(sudoku):
    """
    Expands the sudoku substituting the 0s with the possible values
    """
    sudoku_expanded = sudoku
    for i in range(len(sudoku)):
        for j in range(len(sudoku)):
            if sudoku[i][j] == 0:
                sudoku_expanded[i][j] = list(range(1, len(sudoku)+1))
            else:
                sudoku_expanded[i][j] = [sudoku[i][j]]
    return sudoku_expanded


def check_rows(sudoku_expanded):
    """
    Checks the rows for possible values
    """
    for i in range(len(sudoku_expanded)):
        known_row_values = []
        for j in range(len(sudoku_expanded)):  # Check for known values
            # if the value is already known
            if (len(sudoku_expanded[i][j]) == 1):
                # add it to the list of known values
                known_row_values.append(sudoku_expanded[i][j][0])
        for j in range(len(sudoku_expanded)):  # remove known values from possible values
            if (len(sudoku_expanded[i][j]) > 1):  # if the value is not known
                for k in range(len(known_row_values)):  # remove known values
                    try:
                        sudoku_expanded[i][j].remove(known_row_values[k])
                    except:
                        pass
    return sudoku_expanded


def check_columns(sudoku_expanded):
    """
    Checks the columns for possible values
    """
    for i in range(len(sudoku_expanded)):
        known_column_values = []
        for j in range(len(sudoku_expanded)):  # Check for known values
            # if the value is already known
            if (len(sudoku_expanded[j][i]) == 1):
                # add it to the list of known values
                known_column_values.append(sudoku_expanded[j][i][0])
        for j in range(len(sudoku_expanded)):  # remove known values from possible values
            if (len(sudoku_expanded[j][i]) > 1):  # if the value is not known
                for k in range(len(known_column_values)):  # remove known values
                    try:
                        # print("removing",known_column_values[k],"from",sudoku_expanded[j][i],"at",i,j)
                        sudoku_expanded[j][i].remove(known_column_values[k])
                        # print("removed",known_column_values[k],"from",sudoku_expanded[j][i],"at",i,j)
                    except:
                        # print(e)
                        pass
    return sudoku_expanded


def check_squares_4(sudoku_expanded):
    """
    Checks the squares for possible values for a 4x4 sudoku
    """
    # 0,0 0,1 1,0 1,1   0,2 0,3 1,2 1,3   2,0 2,1 3,0 3,1   2,2 2,3 3,2 3,3
    known_square_values = []
    for square in range(4):
        known_square_values.append([])
        for i in range(0, 2):
            for j in range(0, 2):
                # print(i+int(square%2)*2,j+int(square/2)*2)
                i2 = i+int(square % 2)*2
                j2 = j+int(square/2)*2
                if(len(sudoku_expanded[i2][j2]) == 1):
                    known_square_values[square].append(
                        sudoku_expanded[i2][j2][0])

    # print(known_square_values)
    for square in range(4):
        for i in range(0, 2):
            for j in range(0, 2):
                # print(i+int(square%2)*2,j+int(square/2)*2)
                i2 = i+int(square % 2)*2
                j2 = j+int(square/2)*2
                if(len(sudoku_expanded[i2][j2]) > 1):
                    # remove known values
                    for k in range(len(known_square_values[square])):
                        try:
                            # print("removing",known_square_values[square][k],"from",sudoku_expanded[j][i],"at",i,j)
                            sudoku_expanded[i2][j2].remove(
                                known_square_values[square][k])
                        except:
                            pass
    return sudoku_expanded


def check_squares(sudoku_expanded):
    """
    checks the squares for a generic size sudoku
    """
    known_square_values = []
    sqrt_len = int(len(sudoku_expanded)**0.5)
    for square in range(len(sudoku_expanded)):
        known_square_values.append([])
        for i in range(0, sqrt_len):
            for j in range(0, sqrt_len):
                i2 = i+int(square % sqrt_len)*sqrt_len
                j2 = j+int(square/sqrt_len)*sqrt_len
                if(len(sudoku_expanded[i2][j2]) == 1):
                    known_square_values[square].append(
                        sudoku_expanded[i2][j2][0])

    for square in range(len(sudoku_expanded)):
        for i in range(0, sqrt_len):
            for j in range(0, sqrt_len):
                i2 = i+int(square % sqrt_len)*sqrt_len
                j2 = j+int(square/sqrt_len)*sqrt_len
                if(len(sudoku_expanded[i2][j2]) > 1):
                    # remove known values
                    for k in range(len(known_square_values[square])):
                        try:
                            sudoku_expanded[i2][j2].remove(
                                known_square_values[square][k])
                        except:
                            pass
    return sudoku_expanded


def check_sudoku(sudoku_expanded):
    """
    Checks the sudoku for possible values
    """
    # print_sudoku(sudoku_expanded)
    sudoku_expanded = check_rows(sudoku_expanded)
    # print("rows")
    # print_sudoku(sudoku_expanded)
    # print("columns")
    sudoku_expanded = check_columns(sudoku_expanded)
    # print_sudoku(sudoku_expanded)
    # print("squares")
    sudoku_expanded = check_squares(sudoku_expanded)
    # print_sudoku(sudoku_expanded)
    return sudoku_expanded


def is_solved(sudoku_expanded):
    """
    Checks if the sudoku is solved
    """
    for i in range(len(sudoku_expanded)):
        for j in range(len(sudoku_expanded)):
            if len(sudoku_expanded[i][j]) > 1:
                return False
    return True


def is_valid(sudoku_expanded):
    """
    Checks if the sudoku is valid
    """
    for i in range(len(sudoku_expanded)):
        for j in range(len(sudoku_expanded)):
            if len(sudoku_expanded[i][j]) == 0:
                return False
    return True


def print_sudoku(sudoku_expanded):
    """
    Prints the sudoku
    """
    print("Sudoku:")
    for i in range(len(sudoku_expanded)):
        for j in range(len(sudoku_expanded)):
            for k in range(len(sudoku_expanded[i][j])):
                print(sudoku_expanded[i][j][k], end="")
            print(" "*(len(sudoku_expanded) -
                  len(sudoku_expanded[i][j])+1), end="")
        print()
    print()


def solve_sudoku(sudoku_expanded):
    """
    Reduces the sudoku
    """
    for i in range(10):
        sudoku_expanded = check_sudoku(sudoku_expanded)
    
    if(is_solved(sudoku_expanded)):
        return sudoku_expanded
    
    # if not solved yet, try to solve it by guessing
    i = random.randint(0, len(sudoku_expanded)-1)
    j = random.randint(0, len(sudoku_expanded)-1)
    copy_sudoku_expanded = sudoku_expanded.copy()
    copy_sudoku_expanded[i][j] = [random.choice(sudoku_expanded[i][j])]

    if is_solved(copy_sudoku_expanded):
        return copy_sudoku_expanded
    solve_sudoku(copy_sudoku_expanded)
    return sudoku_expanded


def solve_sudoku_old(sudoku_expanded):
    """
    Solves the sudoku
    """
    counter = 0
    while not is_solved(sudoku_expanded):
        sudoku_expanded = check_sudoku(sudoku_expanded)
        counter += 1
        if(counter > 10):
            i = random.randint(0, len(sudoku_expanded)-1)
            j = random.randint(0, len(sudoku_expanded)-1)
            print("randomly choosing", i, j, "with", sudoku_expanded[i][j])
            choice = random.choice(sudoku_expanded[i][j])
            print("choosing", choice)
            copy_sudoku_expanded = sudoku_expanded.copy()
            copy_sudoku_expanded[i][j] = [choice]
            copy_sudoku_expanded = solve_sudoku(copy_sudoku_expanded)
            if is_solved(copy_sudoku_expanded):
                return copy_sudoku_expanded

    return sudoku_expanded


sudoku_expanded = expand_sudoku(sudoku)
print_sudoku(sudoku_expanded)
sudoku_expanded = solve_sudoku(sudoku_expanded)
print_sudoku(sudoku_expanded)


# check_sudoku(expand_sudoku(sudoku))
