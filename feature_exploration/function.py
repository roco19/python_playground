def fibonacci_recursiva(n):
    if n == 0 or n == 1:
        return n
    return fibonacci_recursiva(n-1) + fibonacci_recursiva(n-2)

def fibonacci_secuencial(n):
    if n == 0 or n == 1:
        return n

    a = 0 # n-2
    b = 1 # n-1

    for i in range(n - 1):
        c = b + a
        a = b
        b = c

    return b

def string_mas_larga(*words):
    max_size = 0
    result = None
    for word in words:
        size = len(word)
        if size > max_size:
            max_size = size
            result = word

    return result

def suma(nums):
    sum = 0
    for num in nums:
        sum += num

    return sum

def es_impar(num):
    return num % 2 != 0

def to_upper(text):
    result = ""
    for char in text:
        if "a" <= char <= "z":
            result += chr(ord(char) - 32)
        else:
            result += char

    return result

def main():
    print(string_mas_larga("234523452345234523452345", "sdfgsdfgsdfg", "asdfasdfasdfasdf"))
    print(suma([1, 2, 3, 4, 5, 20]))
    print(es_impar(3))
    print(es_impar(24))

if __name__ == "__main__":
    main()