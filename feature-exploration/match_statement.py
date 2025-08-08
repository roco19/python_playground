# Simple literal case
def http_error(status: int):
    match status:
        case 200:
            return "Success"
        case 400:
            return "Error"
        case 404:
            return "Not found"
        case _:
            return "This is the default case"

# Example with a tuple, we can use unpacking
def print_point_info(point:tuple[int, int]):
    match point:
        case (0, 0):
            print("This is the origin")
        case (x, 5):
            print(f"X is {x} and Y is 5 - second case")
        case (5, y):
            print(f"X is 5 and Y is {y} - first case")
        case(x, y):
            print(f"X is {x} and Y is {y} - both")
        case _:
            print("This is the default case")

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def main():
    print(http_error(200))
    print(http_error(404))
    print(http_error(500))
    print_point_info((0, 0))
    print_point_info((2, 2))
    print_point_info((5, 5))

if __name__ == "__main__":
    main()