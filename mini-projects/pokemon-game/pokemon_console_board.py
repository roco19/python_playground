"""
Goal of the game is to win all pokemon masters.
"""

import os
import readchar
import pokeload
import random

MAP_DRAW = """\
##############################
#                            #
# ##########          ###### #
# ##########          ###### #
#                     ###### #
#                            #
#                            #
#                            #
                              
                              
# ###                    ### #
# ###                    ### #
# ###         ##         ### #
# ###        ####        ### #
# ###         ##         ### #
# ###                    ### #
# ###########    ########### #
# ###########    ########### #
#                            #
##############################\
"""

PLAYER_BASE = {
    "name": "",
    "position": [],
    "pokemon": None,
    "is_defeated": False
}
INITIAL_POSITION = [1, 1]
ROW = 0
COL = 1

def create_board():
    board_map = [list(line) for line in MAP_DRAW.split("\n")]
    return {
        "map": board_map,
        "height": len(board_map),
        "width": len(board_map[0])
    }

def create_player():
    new_player = dict(PLAYER_BASE)
    new_player["name"] = "player 1"
    new_player["position"] = INITIAL_POSITION
    new_player["pokemon"] = pokeload.get_pokemon_by_id(25) # Pikachu - 25
    return new_player

def create_pokemon_masters():
    pokemon_master_1 = dict(PLAYER_BASE)
    pokemon_master_1["name"] = "Federico"
    pokemon_master_1["position"] = [1, 28]
    pokemon_master_1["pokemon"] = pokeload.get_random_pokemon()

    pokemon_master_2 = dict(PLAYER_BASE)
    pokemon_master_2["name"] = "Roku"
    pokemon_master_2["position"] = [5, 11]
    pokemon_master_2["pokemon"] = pokeload.get_random_pokemon()

    pokemon_master_3 = dict(PLAYER_BASE)
    pokemon_master_3["name"] = "Momo"
    pokemon_master_3["position"] = [10, 15]
    pokemon_master_3["pokemon"] = pokeload.get_random_pokemon()

    pokemon_master_4 = dict(PLAYER_BASE)
    pokemon_master_4["name"] = "Jackie"
    pokemon_master_4["position"] = [14, 24]
    pokemon_master_4["pokemon"] = pokeload.get_random_pokemon()

    return [pokemon_master_1, pokemon_master_2, pokemon_master_3, pokemon_master_4]

def print_board(board, player, pokemon_masters):
    os.system("cls") # Clean board first
    player_position = player["position"]
    board_map = board["map"]
    for row in range(board["height"]):
        for col in range(board["width"]):
            # Code to determine what will be printed in the console
            is_wall = False
            is_player = False
            is_pokemon_master = False

            if board_map[row][col] == "#":
                is_wall = True

            if player_position[ROW] == row and player_position[COL] == col:
                is_player = True

            for pokemon_master in pokemon_masters:
                pokemon_master_position = pokemon_master["position"]
                if pokemon_master_position[ROW] == row and pokemon_master_position[COL] == col:
                    is_pokemon_master = True

            if is_wall:
                char_to_draw = "#"
            elif is_player:
                char_to_draw = "J"
            elif is_pokemon_master:
                char_to_draw = "M"
            else:
                char_to_draw = " "

            print(" {} ".format(char_to_draw), end="")
        print()

def catch_event(board, player, pokemon_masters):
    direction = readchar.readkey()
    if direction == "Q":
        exit()

    next_position = get_next_position(board, player, direction)
    if next_position:
        object_in_position = get_object_in_position(board, player, pokemon_masters, next_position)
        if object_in_position == "wall":
            pass # Do nothing
        elif object_in_position == "master":
            # Let's start the fight
            print("So you want to challenge me, huh? Let's fight.")
            pokemon_master = get_pokemon_master_by_position(pokemon_masters, next_position)
            print(get_pokemon_master_info(pokemon_master))
            input("Press Enter to continue...")

            player_pokemon = player["pokemon"]
            master_pokemon = pokemon_master["pokemon"]
            while player_pokemon["current_health"] > 0 and master_pokemon["current_health"] > 0:
                player_attack(player["pokemon"], pokemon_master["pokemon"])

                if master_pokemon["current_health"] > 0:
                    enemy_attack(pokemon_master["pokemon"], player["pokemon"])

            if player_pokemon["current_health"] == 0:
                print()
                print("Haha you've lost, come back when you're stronger.")
                # Let's reset pokemons health since there are no hospitals in this game.
                player_pokemon["current_health"] = player_pokemon["base_health"]
                master_pokemon["current_health"] = master_pokemon["base_health"]
            else:
                print()
                print("You're stronger than I thought. You've won.")
                pokemon_masters.remove(pokemon_master)

            input("Press Enter to continue...")
            pass
        elif object_in_position == "empty":
            player["position"] = next_position
        else:
            print("This case should not happen. Debug your code.")

def get_next_position(board, player, direction):
    next_position = None
    player_position = player["position"]
    if direction == "w":
        next_position = [player_position[ROW] - 1, player_position[COL]]
        if next_position[ROW] < 0:
            next_position[ROW] = board["height"] - 1
    elif direction == "a":
        next_position = [player_position[ROW], player_position[COL] - 1]
        if next_position[COL] < 0:
            next_position[COL] = board["width"] - 1
    elif direction == "s":
        next_position = [player_position[ROW] + 1, player_position[COL]]
        if next_position[ROW] > board["height"] - 1:
            next_position[ROW] = 0
    elif direction == "d":
        next_position = [player_position[ROW], player_position[COL] + 1]
        if next_position[COL] > board["width"] - 1:
            next_position[COL] = 0
    return next_position

def get_object_in_position(board, player, pokemon_masters, position):
    pokemon_master = get_pokemon_master_by_position(pokemon_masters, position)
    if pokemon_master:
        return "master"

    if player["position"] == position:
        return "player"

    object_in_board = board["map"][position[ROW]][position[COL]]
    if object_in_board == "#":
        return "wall"
    else:
        return "empty"

def get_pokemon_master_by_position(pokemon_masters, position):
    for pokemon_master in pokemon_masters:
        if pokemon_master["position"] == position:
            return pokemon_master

    return None

def get_pokemon_master_info(pokemon_master):
    return f"Master '{pokemon_master["name"]}' ({pokeload.get_pokemon_info(pokemon_master["pokemon"])})"

def player_attack(player_pokemon, enemy_pokemon):
    selected_attack = choose_attack(player_pokemon)
    total_damage = selected_attack["damage"]

    enemy_pokemon["current_health"] = max(enemy_pokemon["current_health"] - total_damage, 0)
    print()
    print(f"{player_pokemon["name"]} has use {selected_attack["name"]}. Total damage: {total_damage}.")
    print(f"Enemy pokemon status: {pokeload.get_pokemon_info(enemy_pokemon)}")
    if enemy_pokemon["current_health"] == 0:
        print("Pokemon defeated. Congrats!")
    input("Press Enter to continue...")

def enemy_attack(enemy_pokemon, player_pokemon):
    selected_attack = choose_random_attack(enemy_pokemon)
    total_damage = selected_attack["damage"]

    player_pokemon["current_health"] = max(player_pokemon["current_health"] - total_damage, 0)
    print()
    print(f"{enemy_pokemon["name"]} has use {selected_attack["name"]}. Total damage: {total_damage}.")
    print(f"Player pokemon status: {pokeload.get_pokemon_info(player_pokemon)}")
    if player_pokemon["current_health"] == 0:
        print("Your pokemon has been defeated!")
    input("Press Enter to continue...")

def choose_attack(pokemon):
    print()
    print("- Pokemon attacks -")
    for i, attack in enumerate(pokemon["attacks"]):
        print(f"[{i}] {pokeload.get_attack_info(attack)}")

    while True:
        player_selection = input("Choose an attack: ")
        try:
            return pokemon["attacks"][int(player_selection)]
        except (ValueError, IndexError):
            print("Invalid selection.")

def choose_random_attack(pokemon):
    return random.choice(pokemon["attacks"])

def main():
    board = create_board()
    player = create_player()
    pokemon_masters = create_pokemon_masters()

    while pokemon_masters:
        print_board(board, player, pokemon_masters)
        catch_event(board, player, pokemon_masters)

    print()
    print("-- You've defeated all the pokemon masters. Congratulations, you've won! --")


if __name__ == '__main__':
    main()