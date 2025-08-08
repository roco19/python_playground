def matrix_transpose(matrix: list[list]) -> list[list]:
    transposed_matrix = []
    for col in range(len(matrix[0])):
        transposed_matrix.append([])
        for row in range(len(matrix)):
            transposed_matrix[col].append(matrix[row][col])
    return transposed_matrix

def matrix_transpose_2(matrix: list[list]) -> list[list]:
    return [[matrix[row][col] for row in range(len(matrix))] for col in range(len(matrix[0]))]

def matrix_transpose_3(matrix: list[list]) -> list[list]:
    return [list(row) for row in zip(*matrix)]

def matrix_vertical_flip(matrix: list[list]) -> list[list]:
    return [row[::-1] for row in matrix]

def matrix_horizontal_flip(matrix: list[list]) -> list[list]:
    return matrix[::-1]

def rotate_90_right(matrix: list[list]) -> list[list]:
    rotated_matrix = [[0 for _ in range(len(matrix))] for _ in range(len(matrix[0]))]
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            rotated_matrix[col][len(matrix) - 1 - row] = matrix[row][col]
    return rotated_matrix

def rotate_90_right_2(matrix: list[list]) -> list[list]:
    return matrix_vertical_flip(matrix_transpose_2(matrix))

def rotate_90_right_3(matrix: list[list]) -> list[list]:
    return [list(row) for row in zip(*matrix_horizontal_flip(matrix))]

def rotate_90_left(matrix: list[list]) -> list[list]:
    return [list(row) for row in zip(*matrix_vertical_flip(matrix))]

def clean_matrix(matrix: list[list], default_value = 0):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            matrix[row][col] = default_value