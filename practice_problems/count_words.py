import re

TEXT = """\
¿Te has preguntado alguna vez cómo contar palabras en Python? Este lenguaje de programación es conocido por su
simplicidad y versatilidad, y contar palabras es una de esas tareas básicas que todo programador debería conocer. En
este artículo, te explicaré cómo hacerlo de manera sencilla y práctica, utilizando diferentes enfoques y técnicas.
¡Vamos allá!

Contar palabras en un texto es una habilidad útil en muchos contextos: desde el procesamiento de datos hasta el análisis
de texto, pasando por la creación de aplicaciones web y scripts automatizados. Entender cómo contar palabras en Python
te permitirá manejar y analizar textos de manera más eficiente.
"""

def count_words(text: str) -> dict:
    # Normalize all words
    text = text.lower()

    # Split all the words
    words = re.findall(r"[\w']+", text)

    # Count the words
    words_map = {}
    for word in words:
        words_map[word] = words_map.get(word, 0) + 1

    return words_map

def main():
    words = count_words(TEXT)
    for word, count in words.items():
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()