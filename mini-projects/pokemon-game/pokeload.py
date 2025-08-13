import pickle
import random
import requests_html


MAX_POKEMON_COUNT = 150
POKEMON_FILE = "pokefile.pkl"
URL_BASE = "https://pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="

POKEMON_BASE = {
    "name": "",
    "level": 1,
    "base_health": 100,
    "current_health": 100,
    "current_exp": 0,
    "type": [],
    "attacks": []
}

# Contains the global list to all the functions.
all_pokemons = None

def init():
    if not all_pokemons:
        _load_all_pokemons()

def _load_all_pokemons():
    global all_pokemons
    try:
        print(f"Loading pokemons from {POKEMON_FILE}.")
        with open(POKEMON_FILE, "rb") as file:
            all_pokemons = pickle.load(file)
        print(f"Loaded {len(all_pokemons)} pokemons.")
    except FileNotFoundError:
        print("File not found. Downloading pokemons from internet...")
        all_pokemons = _request_all_pokemons()
        print(f"Downloaded {len(all_pokemons)} pokemons.")
        with open(POKEMON_FILE, "wb") as file:
            pickle.dump(all_pokemons, file)
    print("Pokemon list ready!")

def _request_all_pokemons():
    requested_pokemons = []
    session = requests_html.HTMLSession()
    for i in range(1, MAX_POKEMON_COUNT + 1):
        pokemon = _request_pokemon(session, i)
        requested_pokemons.append(pokemon)
        print(f"Downloaded: ({i}) {pokemon['name']}")
    session.close()
    return requested_pokemons

def _request_pokemon(session, index):
    pokemon_url = f"{URL_BASE}{index}"
    pokemon_page = session.get(pokemon_url)

    new_pokemon = dict(POKEMON_BASE)
    new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text
    new_pokemon["type"] = [elem.attrs["alt"] for elem in pokemon_page.html.find(".bordeambos", first=True).find("img")]
    new_pokemon["attacks"] = [_get_attack(attack_elem) for attack_elem in pokemon_page.html.find("table.pkmain")[-1].find("tr.check3")]
    return new_pokemon

def _get_attack(attack_elem):
    attack = {
        "name": attack_elem.find("a", first=True).text,
        "type": attack_elem.find("img", first=True).attrs["alt"],
        "damage": int(attack_elem.find("td")[3].text.strip().replace("--", "0")),
        "min_level": int(attack_elem.find("th")[1].text or "1")
    }
    return attack

def get_all_pokemons():
    return all_pokemons

def get_pokemon_by_id(index):
    return all_pokemons[index - 1]

def get_random_pokemon():
    return random.choice(all_pokemons)

def get_random_pokemons(num):
    return random.sample(all_pokemons, num)

def get_pokemon_info(pokemon):
    return f"{pokemon["name"]} | lvl {pokemon["level"]} | hp {pokemon["current_health"]}/{pokemon["base_health"]}"

def get_attack_info(attack):
    return f"{attack["name"]} | type {attack["type"]} | damage {attack["damage"]}"

# Ensure the list is initialized before calling any function.
init()

if __name__ == '__main__':
    all_pokemons = get_all_pokemons()
    print(get_random_pokemons(2))