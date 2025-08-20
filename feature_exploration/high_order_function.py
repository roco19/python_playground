# Creating higher order functions
from functools import reduce
from statistics import mean
from typing import Callable


# First type: function that receives a function as an argument.
def apply_function(function: Callable[[int], int], n: int) -> int:
    return function(n)

def square(n: int) -> int:
    return n * n

print(apply_function(square, 5))


# Second type: function that returns another function (also called Closure).
def apply_multiplier(n: int) -> Callable[[int], int]:
    def multiplier(m : int) -> int:
        return n * m
    return multiplier

print(apply_multiplier(5)(8))


# Builtin higher order functions.
numbers = [5, 2, 6, 9, 10]
print(list(map(square, numbers)))
print([square(n) for n in numbers])
print(list(map(lambda x: x * x, numbers)))

print(reduce(lambda x, y: x + y, numbers))


# Example
def log_call(func):
    print(func)
    print(type(func))
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args} [{kwargs}]")
        return func(*args, **kwargs)
    return wrapper

# @log_call
def say_hello(name):
    print(f"Hola, {name}!")
    return "name" + " Hi."

print(say_hello("Rodrigo"))
print("-------")
result = log_call(say_hello)
print(result("Rodrigo"))

"""
Ejercicio con listas de estudiantes
"""

students = [
    {
        "name": "Ana",
        "birthday": "01/01/1990",
        "grades": [7, 8, 9, 10]
    },
    {
        "name": "Ernesto",
        "birthday": "05/03/1995",
        "grades": [10, 10, 9, 8.5]
    },
    {
        "name": "Ignacio",
        "birthday": "05/07/1850",
        "grades": [5, 9, 10, 10]
    },
    {
        "name": "Oscar",
        "birthday": "01/09/1996",
        "grades": [8.5, 9.5, 6, 8]
    },
    {
        "name": "Ursula",
        "birthday": "01/11/1990",
        "grades": [10, 8.5, 9, 9.5]
    }
]

print(list(map(lambda student: {"name": student["name"], "average": sum(student["grades"]) / len(student["grades"])}, students)))
print(list(map(lambda student: {"name": student["name"], "average": mean(student["grades"])}, students)))

new_list = []
for student in students:
    if mean(student["grades"]) >= 9:
        new_list.append(student["name"])
print(new_list)

new_list = list(map(lambda student: student["name"], filter(lambda student: mean(student["grades"]) >= 9, students)))
print(new_list)

new_list = [student["name"] for student in students if mean(student["grades"]) >= 9]
print(new_list)
