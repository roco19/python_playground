from enum import Enum
from readchar import readkey, key
from tetris_matrix_utils import clean_matrix, rotate_90_right, rotate_90_left
import os
import random

NUM_ROWS = 15
NUM_COL = 10

EMPTY_CELL = "🔲 "
CURRENT_SHAPE_CELL = "🔳 "
FROZEN_CELL = "🔳 "

SHAPE_I = [[1, 1, 1, 1]]
SHAPE_J = [[1, 1, 1], [0, 0, 1]]
SHAPE_L = [[0, 0, 1], [1, 1, 1]]
SHAPE_O = [[1, 1], [1, 1]]
SHAPE_S = [[0, 1, 1], [1, 1, 0]]
SHAPE_Z = [[1, 1, 0], [0, 1, 1]]
SHAPE_T = [[0, 1, 0], [1, 1, 1]]
SHAPES = [SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_Z, SHAPE_T]

SHAPE_INIT_POS = (0, 3)

class Direction(Enum):
    QUIT = "q"
    LEFT = key.LEFT
    RIGHT = key.RIGHT
    DOWN = key.DOWN
    ROTATE_L = "z"
    ROTATE_R = "x"

def create_initial_board() -> list[list]:
    board = [[EMPTY_CELL for _ in range(NUM_COL)] for _ in range(NUM_ROWS)]
    return board

def create_frozen_matrix() -> list[list]:
    frozen_matrix = [[0 for _ in range(NUM_COL)] for _ in range(NUM_ROWS)]
    return frozen_matrix

def clean_board(board: list[list]):
    clean_matrix(board, EMPTY_CELL)

def get_new_shape() -> dict:
    shape = random.choice(SHAPES)
    return {
        "shape": shape,
        "row": SHAPE_INIT_POS[0],
        "col": SHAPE_INIT_POS[1],
    }

def print_board(board: list[list], current_shape: dict, frozen_shapes: list[list]):
    os.system("cls")
    clean_board(board)
    for row in range(len(board)):
        for col in range(len(board[0])):
            add_shape_to_matrix(board, current_shape, CURRENT_SHAPE_CELL)
            add_frozen_shapes_to_matrix(board, frozen_shapes, FROZEN_CELL)
            print(board[row][col], end="")
        print()

def add_shape_to_matrix(board: list[list], current_shape: dict, cell_content):
    board_row = current_shape["row"]
    board_col = current_shape["col"]
    for i in range(len(current_shape["shape"])):
        for j in range(len(current_shape["shape"][0])):
            if current_shape["shape"][i][j]:
                board[board_row + i][board_col + j] = cell_content

def add_frozen_shapes_to_matrix(board: list[list], frozen_shapes: list[list], cell_content):
    for i in range(NUM_ROWS):
        for j in range(NUM_COL):
            if frozen_shapes[i][j]:
                board[i][j] = cell_content

def get_user_movement():
    direction = readkey()
    try:
        return Direction(direction)
    except ValueError:
        return None

# TODO: Add validations to avoid moving to frozen shapes.
def move_shape(move, current_shape: dict, frozen_shapes: list[list]):
    match move:
        case Direction.QUIT:
            exit()
        case Direction.LEFT:
            if current_shape["col"] == 0:
                return

            can_move_left = True
            shape_height = len(current_shape["shape"])
            shape_width = len(current_shape["shape"][0])
            for i in range(shape_height):
                for j in range(shape_width):
                    if current_shape["shape"][i][j]:
                        if frozen_shapes[current_shape["row"] + i ][current_shape["col"] + j - 1]:
                            can_move_left = False
                            break
                if not can_move_left:
                    break

            if can_move_left:
                current_shape["col"] -= 1

        case Direction.RIGHT:
            shape_width = len(current_shape["shape"][0])
            if (current_shape["col"] + shape_width) == NUM_COL:
                return

            can_move_right = True
            shape_height = len(current_shape["shape"])
            shape_width = len(current_shape["shape"][0])
            for i in range(shape_height):
                for j in range(shape_width):
                    if current_shape["shape"][i][j]:
                        if frozen_shapes[current_shape["row"] + i ][current_shape["col"] + j + 1]:
                            can_move_right = False
                            break
                if not can_move_right:
                    break

            if can_move_right:
                current_shape["col"] += 1

        case Direction.DOWN:
            shape_height = len(current_shape["shape"])
            if (current_shape["row"] + shape_height) < NUM_ROWS:
                current_shape["row"] += 1
        case Direction.ROTATE_L:
            shape_width = len(current_shape["shape"][0])
            shape_height = len(current_shape["shape"])
            if (current_shape["col"] + shape_height - 1) < NUM_COL and (current_shape["row"] + shape_width - 1) < NUM_ROWS:
                current_shape["shape"] = rotate_90_left(current_shape["shape"])
        case Direction.ROTATE_R:
            shape_width = len(current_shape["shape"][0])
            shape_height = len(current_shape["shape"])
            if (current_shape["col"] + shape_height - 1) < NUM_COL and (current_shape["row"] + shape_width - 1) < NUM_ROWS:
                current_shape["shape"] = rotate_90_right(current_shape["shape"])

def freeze_shapes(current_shape: dict, frozen_shapes: list[list]) -> bool:
    shape_height = len(current_shape["shape"])
    if (current_shape["row"] + shape_height) == NUM_ROWS:
        add_shape_to_matrix(frozen_shapes, current_shape, 1)
        return True

    can_move_down = True
    shape_width = len(current_shape["shape"][0])
    for i in range(shape_height):
        for j in range(shape_width):
            if current_shape["shape"][i][j]:
                if frozen_shapes[current_shape["row"] + i + 1][current_shape["col"] + j]:
                    can_move_down = False
                    add_shape_to_matrix(frozen_shapes, current_shape, 1)
                    break
        if not can_move_down:
            break

    # If we can't move down then let's freeze the shape
    return not can_move_down


def clear_full_rows(frozen_shapes: list[list]):
    new_matrix = [row for row in frozen_shapes if any(item == 0 for item in row)]
    num_removed_rows = len(frozen_shapes) - len(new_matrix)
    new_rows = [[0] * len(frozen_shapes[0]) for _ in range(num_removed_rows)]
    frozen_shapes[:] = new_rows + new_matrix

def main():
    board = create_initial_board()
    frozen_shapes = create_frozen_matrix()
    current_shape = get_new_shape()

    while True:
        print_board(board, current_shape, frozen_shapes) # current_shape, existing_shapes
        move = get_user_movement()
        if move:
            move_shape(move, current_shape, frozen_shapes)
            if freeze_shapes(current_shape, frozen_shapes):
                current_shape = get_new_shape()
                clear_full_rows(frozen_shapes)


if __name__ == "__main__":
    main()