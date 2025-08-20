"""
 * Crea un programa que comprueba si los paréntesis, llaves y corchetes
 * de una expresión están equilibrados.
 * - Equilibrado significa que estos delimitadores se abren y cieran
 *   en orden y de forma correcta.
 * - Paréntesis, llaves y corchetes son igual de prioritarios.
 *   No hay uno más importante que otro.
 * - Expresión balanceada: { [ a * ( c + d ) ] - 5 }
 * - Expresión no balanceada: { a * ( c + d ) ] - 5 }
"""

def is_balanced(expression: str):
    """
    Checks if the given expression has balanced parentheses, brackets, and braces.
    """
    bracket_map = {")": "(", "]": "[", "}": "{"}
    opening_brackets = set(bracket_map.values())
    stack = []

    for c in expression:
        if c in opening_brackets:
            stack.append(c)
        elif c in bracket_map:
            if not stack or bracket_map[c] != stack.pop():
                return False

    return not stack

def main():
    print(f"Balanced: {is_balanced("{ [ a * ( c + d  )] - 5 }")}")

if __name__ == "__main__":
    main()