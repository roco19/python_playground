import speak_and_listen
import random
from requests_html import HTMLSession
from PIL import Image
from io import BytesIO

MAIN_SITE_LINK = "https://aquaplantasmx.com"
ROUND_NUM = 3
MODE = 0 # 0 - console, 1 - audio

def main():
    text_out("Bienvenido al precio justo! El juego en el que tienes que adivinar el precio correcto!")
    text_out("El juego constará de 5 rondas. El que gane más rondas, ganará el juego.")

    session = HTMLSession()
    categories = get_categories(session)

    player1_wins = 0
    player2_wins = 0

    for i in range(ROUND_NUM):
        text_out(f"Ronda {i+1}")
        category_url = select_category(categories)
        product = choose_random_product(session, category_url)
        show_product_image(session, product)
        text_out("El producto seleccionado es: " + product["title"])

        if i % 2 == 0:
            text_out("Jugador 1. ¿Cuánto crees que vale el producto? ")
            player1_guess = float(text_in())

            text_out("Jugador 2. ¿Cuánto crees que vale el producto? ")
            player2_guess = float(text_in())
        else:
            text_out("Jugador 2. ¿Cuánto crees que vale el producto? ")
            player2_guess = float(text_in())

            text_out("Jugador 1. ¿Cuánto crees que vale el producto? ")
            player1_guess = float(text_in())


        player1_diff = abs(product["price"] - player1_guess)
        player2_diff = abs(product["price"] - player2_guess)

        if player1_diff == player2_diff:
            text_out("Esta ronda es un empate.")
        elif player1_diff < player2_diff:
            text_out("Ronda ganada por el jugador 1.")
            player1_wins += 1
        else:
            text_out("Ronda ganada por el jugador 2.")
            player2_wins += 1

        text_out(f"El precio del producto era de: {product["price"]}")

    session.close()

    if player1_wins == player2_wins:
        text_out("El juego ha terminado en empate, felicidades a los 2.")
    elif player1_wins > player2_wins:
        text_out("El jugador 1 ha ganado. Felicidades!")
    else:
        text_out("El jugador 2 ha ganado. Felicidades!")


def show_product_image(session, product):
    image_page = session.get(product["img_src"])
    image = Image.open(BytesIO(image_page.content))
    image.show()

def get_categories(session):
    main_site = session.get(MAIN_SITE_LINK)

    categories = []
    category_elements = main_site.html.find(".link-item a")
    for category in category_elements:
        category_href = category.attrs["href"]
        category_name = category_href.split("/")[2]
        category_href = MAIN_SITE_LINK + category_href
        if category_href and category_name:
            categories.append({"name": category_name, "href": category_href})

    print(categories)
    return categories

def select_category(categories):
    for i, category in enumerate(categories):
        print(f"{i + 1}. {category['name']}")

    text_out("Selecciona una categoría: ")
    choice = int(text_in()) - 1
    return categories[choice]['href']

def get_player_guess():
    guess = float(input("¿Cuánto crees que vale?: "))
    return guess

def choose_random_product(session, category_url):
    category_page = session.get(category_url)
    products = category_page.html.find(".product-item-wrapper")
    while True:
        product_element = random.choice(products)
        sold_out = product_element.find(".sold_out")
        if not sold_out:
            break

    prod_title = product_element.find(".product-title a", first=True).text
    prod_price = product_element.find(".price", first=True).text
    prod_price = float(prod_price.replace("$", "").replace(",", ""))
    prod_image_src = "https:" + product_element.find("img", first=True).attrs["src"]
    product = {
        "title": prod_title,
        "price": prod_price,
        "img_src": prod_image_src
    }
    return product

def text_out(text):
    if MODE:
        speak_and_listen.speak(text)
    else:
        print(text)

def text_in():
    if MODE:
        return speak_and_listen.listen()
    else:
        return input()

if __name__ == '__main__':
    main()