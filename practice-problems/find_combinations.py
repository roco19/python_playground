GOAL = 6
NUMBERS = [1, 2, 1, 1, 1, 1, 2, 1]

def find_combinations(index, path, numbers, goal, combinations):
    if goal == 0:
        combinations.append(path.copy())
        return

    if goal < 0 or index >= len(numbers):
        return

    for i in range(index, len(NUMBERS)):
        if i > index and NUMBERS[i] == NUMBERS[i - 1]:
            continue

        value = numbers[i]
        path.append(value)
        find_combinations(i + 1, path, numbers, goal - value, combinations)
        path.pop()

if __name__ == '__main__':
    combinations = []
    NUMBERS.sort()
    find_combinations(0, [], NUMBERS, GOAL, combinations)
    print(combinations)