import pokeload
import random

TYPE_EFFECTIVENESS = {
    "normal": {"lucha": 0.5},
    "fuego": {"agua": 0.5, "tierra": 0.5, "roca": 0.5, "planta": 2, "hielo": 2, "bicho": 2, "acero": 2},
    "agua": {"planta": 0.5, "electrico": 0.5, "fuego": 2, "tierra": 2, "roca": 2},
    "planta": {"fuego": 0.5, "hielo": 0.5, "veneno": 0.5, "volador": 0.5, "bicho": 0.5, "agua": 2, "tierra": 2, "roca": 2},
    "electrico": {"tierra": 0, "agua": 2, "volador": 2},
    "hielo": {"fuego": 0.5, "lucha": 0.5, "roca": 0.5, "acero": 0.5, "planta": 2, "tierra": 2, "volador": 2, "dragon": 2},
    "lucha": {"volador": 0.5, "psiquico": 0.5, "hada": 0.5, "normal": 2, "hielo": 2, "roca": 2, "siniestro": 2, "acero": 2},
    "veneno": {"tierra": 0.5, "psiquico": 0.5, "planta": 2, "hada": 2},
    "tierra": {"agua": 0.5, "planta": 0.5, "hielo": 0.5, "fuego": 2, "electrico": 2, "veneno": 2, "roca": 2, "acero": 2},
    "volador": {"electrico": 0.5, "hielo": 0.5, "roca": 0.5, "planta": 2, "lucha": 2, "bicho": 2},
    "psiquico": {"bicho": 0.5, "fantasma": 0.5, "siniestro": 0.5, "lucha": 2, "veneno": 2},
    "bicho": {"volador": 0.5, "roca": 0.5, "fuego": 0.5, "planta": 2, "psiquico": 2, "siniestro": 2},
    "roca": {"agua": 0.5, "planta": 0.5, "lucha": 0.5, "tierra": 0.5, "acero": 0.5, "fuego": 2, "hielo": 2, "volador": 2, "bicho": 2},
    "fantasma": {"siniestro": 0.5, "psiquico": 2, "fantasma": 2},
    "dragon": {"hielo": 0.5, "hada": 0.5, "dragon": 2},
    "siniestro": {"lucha": 0.5, "bicho": 0.5, "hada": 0.5, "psiquico": 2, "fantasma": 2},
    "acero": {"fuego": 0.5, "lucha": 0.5, "tierra": 0.5, "hielo": 2, "roca": 2, "hada": 2},
    "hada": {"veneno": 0.5, "acero": 0.5, "lucha": 2, "dragon": 2, "siniestro": 2},
}

MAX_NUMBER_OF_POKEMONS = 150

def main():
    pokemon_list = get_random_pokemons(MAX_NUMBER_OF_POKEMONS)
    print("\n--- Welcome to Pokemon Survival! ---")
    player_profile = get_player_profile(pokemon_list)

    print(f"\nHello {player_profile["name"]}.")
    print(f"There are a total of {len(pokemon_list)} pokemons to defeat. Let the battles begin!")

    while any_player_pokemon_lives(player_profile) and pokemon_list:
        player_profile["combats"] += 1
        enemy_pokemon = pokemon_list.pop()

        fight(player_profile, enemy_pokemon)
        if any_player_pokemon_lives(player_profile):
            item_lottery(player_profile)

    if not pokemon_list and any_player_pokemon_lives(player_profile):
        print()
        print(f"-- You've defeated every pokemon in the game. Congratulations, after {player_profile["combats"]} combats, you've won! --")
    else:
        print()
        print(f"-- Game over. You've lost in the combat number: {player_profile["combats"]} --")

def get_random_pokemons(num_pokemons):
    all_pokemons = pokeload.get_all_pokemons()
    random.shuffle(all_pokemons)
    return all_pokemons[:num_pokemons]

def get_player_profile(pokemon_list):
    return {
        "name": input("What's your name?: "),
        "pokemon_inventory": [pokemon_list.pop() for _ in range(3)],
        "combats": 0,
        "pokeballs": 1,
        "health_potions": 1
    }

def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0

def fight(player_profile, enemy_pokemon):
    print()
    print(f"Start of combat: {player_profile["combats"]}")

    attack_history = []
    pokemon_caught = False
    player_pokemon = choose_pokemon(player_profile)
    print()
    print(f"Opponents: ({get_pokemon_info(player_pokemon)}) VS ({get_pokemon_info(enemy_pokemon)})")


    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:
        action = None
        while action not in ["A", "P", "H", "S"]:
            print()
            action = input("What do you want to do? [A]ttack, [P]okeball, [H]ealth potion, [S]witch pokemon, Show [I]nventory, [Q]uit game: ")

            # Show inventory doesn't consume the turn
            if action == "I":
                show_inventory(player_profile)
            elif action == "Q":
                print("Goodbye!")
                exit()
            elif player_pokemon["current_health"] == 0 and action not in ["H", "S"]:
                action = None
                print("You need to heal or switch your pokemon before continuing.")

        if action == "A":
            player_attack(player_pokemon, enemy_pokemon)
            attack_history.append(player_pokemon)
        elif action == "P":
            # If the enemy pokemon is caught then the battle ends. Let's break the loop.
            if capture_with_pokeball(player_profile, enemy_pokemon):
                pokemon_caught = True
                break
            input("Press Enter to continue...")
        elif action == "H":
            # If the pokemon is not healed then let's give the player another action.
            if not cure_pokemon(player_profile, player_pokemon):
                continue
        elif action == "S":
            # Here we can only choose healthy pokemons
            player_pokemon = choose_healthy_pokemon(player_profile)
            print()
            print(f"Opponents: ({get_pokemon_info(player_pokemon)}) VS ({get_pokemon_info(enemy_pokemon)})")
            input("Press Enter to continue...")

        if enemy_pokemon["current_health"] > 0:
            enemy_attack(enemy_pokemon, player_pokemon)

        # Let's give the player the chance to change their pokemon without loosing a turn.
        if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile):
            print()
            print("You can choose a different pokemon or keep your current pokemon to heal it.")
            player_pokemon = choose_pokemon(player_profile)

    if enemy_pokemon["current_health"] == 0 or pokemon_caught:
        print()
        print("You have won the combat, congrats!")
        assign_experience(attack_history)
    elif not any_player_pokemon_lives(player_profile):
        print()
        print("You have lost all your pokemon. You have lost the battle.")

    print(f"End of combat: {player_profile["combats"]}")
    input("Press Enter to continue...")

def choose_pokemon(player_profile):
    print("- Player pokemons -")
    for i, pokemon in enumerate(player_profile["pokemon_inventory"]):
        print(f"[{i}] {get_pokemon_info(pokemon)}")
    while True:
        player_selection = input("Choose the pokemon you want to battle: ")
        try:
            return player_profile["pokemon_inventory"][int(player_selection)]
        except (ValueError, IndexError):
            print("Invalid selection.")

def choose_healthy_pokemon(player_profile):
    # Filter pokemons
    available_pokemon = [pokemon for pokemon in player_profile["pokemon_inventory"] if pokemon["current_health"] > 0]

    print("- Player pokemons -")
    for i, pokemon in enumerate(available_pokemon):
        print(f"[{i}] {get_pokemon_info(pokemon)}")
    while True:
        player_selection = input("Choose the pokemon you want to battle: ")
        try:
            return available_pokemon[int(player_selection)]
        except (ValueError, IndexError):
            print("Invalid selection.")

def choose_attack(pokemon):
    # Filter available attacks
    available_attacks = [attack for attack in pokemon["attacks"] if attack["min_level"] <= pokemon["level"]]

    print("- Pokemon attacks -")
    for i, attack in enumerate(available_attacks):
        print(f"[{i}] {get_attack_info(attack)}")

    while True:
        player_selection = input("Choose an attack: ")
        try:
            return available_attacks[int(player_selection)]
        except (ValueError, IndexError):
            print("Invalid selection.")

def choose_random_attack(pokemon):
    # Filter available attacks
    available_attacks = [attack for attack in pokemon["attacks"] if attack["min_level"] <= pokemon["level"]]
    return random.choice(available_attacks)

def get_pokemon_info(pokemon):
    return f"{pokemon["name"]} | lvl {pokemon["level"]} | hp {pokemon["current_health"]}/{pokemon["base_health"]}"

def get_attack_info(attack):
    return f"{attack["name"]} | type {attack["type"]} | damage {attack["damage"]}"

def player_attack(player_pokemon, enemy_pokemon):
    selected_attack = choose_attack(player_pokemon)
    damage_multiplier = calculate_type_multiplier(selected_attack["type"], enemy_pokemon["type"])
    total_damage = int(selected_attack["damage"] * damage_multiplier)

    enemy_pokemon["current_health"] = max(enemy_pokemon["current_health"] - total_damage, 0)
    print()
    print(f"{player_pokemon["name"]} has use {selected_attack["name"]}. Total damage: {total_damage}. Type multiplier: {damage_multiplier}")
    print(f"Enemy pokemon status: {get_pokemon_info(enemy_pokemon)}")
    if enemy_pokemon["current_health"] == 0:
        print("Pokemon defeated. Congrats!")
    input("Press Enter to continue...")

def enemy_attack(enemy_pokemon, player_pokemon):
    selected_attack = choose_random_attack(enemy_pokemon)
    damage_multiplier = calculate_type_multiplier(selected_attack["type"], player_pokemon["type"])
    total_damage = int(selected_attack["damage"] * damage_multiplier)

    player_pokemon["current_health"] = max(player_pokemon["current_health"] - total_damage, 0)
    print()
    print(f"{enemy_pokemon["name"]} has use {selected_attack["name"]}. Total damage: {total_damage}. Type multiplier: {damage_multiplier}")
    print(f"Player pokemon status: {get_pokemon_info(player_pokemon)}")
    if player_pokemon["current_health"] == 0:
        print("Your pokemon has been defeated!")
    input("Press Enter to continue...")

def assign_experience(attack_history):
    for pokemon in attack_history:
        points = random.randint(1, 5)
        pokemon["current_exp"] += points

        while pokemon["current_exp"] > 20:
            pokemon["current_exp"] -= 20
            pokemon["level"] += 1
            pokemon["current_health"] = pokemon["base_health"]
            print(f"Your pokemon has leveled up: {get_pokemon_info(pokemon)}")

def cure_pokemon(player_profile, player_pokemon):
    if player_profile["health_potions"] == 0:
        print("There are no potions left.")
        return False

    if player_pokemon["current_health"] >= player_pokemon["base_health"]:
        print("You pokemon is already at full health.")
        return False

    player_pokemon["current_health"] += 50
    if player_pokemon["current_health"] > player_pokemon["base_health"]:
        player_pokemon["current_health"] = player_pokemon["base_health"]

    player_profile["health_potions"] -= 1
    print(f"You pokemon has been healed. You now have {player_profile["health_potions"]} health potions left.")
    print(f"Healed pokemon: {get_pokemon_info(player_pokemon)}")
    input("Press Enter to continue...")
    return True

def capture_with_pokeball(player_profile, enemy_pokemon):
    pokemon_caught = False

    if player_profile["pokeballs"] == 0:
        print("There are no pokeballs left.")
        return pokemon_caught

    player_profile["pokeballs"] -= 1
    catch_probability = (100 - enemy_pokemon["current_health"]) / 100
    if random.random() < catch_probability:
        pokemon_caught = True
        player_profile["pokemon_inventory"].append(enemy_pokemon)
        print(f"You have caught the pokemon, congrats! You now have {player_profile["pokeballs"]} pokeballs left.")
    else:
        print(f"Bad luck, you couldn't catch the pokemon. You now have {player_profile["pokeballs"]} pokeballs left.")

    return pokemon_caught

def item_lottery(player_profile):
    # Both pokeball and life potion have a 10% chance.
    if random.random() < 0.1:
        print()
        print("- You have won a pokeball.")
        player_profile["pokeballs"] += 1

    if random.random() < 0.1:
        print()
        print("- Congrats! You have won a health potion.")
        player_profile["health_potions"] += 1

def show_inventory(player_profile):
    print("Here's your inventory:")
    print(f"- Pokeballs: {player_profile["pokeballs"]}")
    print(f"- Health potions: {player_profile["health_potions"]}")
    print("- Pokemons:")
    for pokemon in player_profile["pokemon_inventory"]:
        print(f"  - {get_pokemon_info(pokemon)}")

def calculate_type_multiplier(attack_type, enemy_types):
    multiplier = 1.0
    for enemy_type in enemy_types:
        multiplier *= TYPE_EFFECTIVENESS[attack_type].get(enemy_type, 1.0)
    return multiplier


if __name__=="__main__":
    main()