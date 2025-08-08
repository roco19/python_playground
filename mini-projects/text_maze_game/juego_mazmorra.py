import time
import random

def print_pause(text):
    time.sleep(0)
    print(text)

has_sword = False
has_wound = False

print("---------------------------\n"
      "- El juego de la mazmorra -\n"
      "---------------------------\n")

# Intro
print_pause("Te despiertas en una mazmorra oscura y húmeda.")
print_pause("Una antorcha parpadea débilmente en la pared.")
print_pause("Tienes una fuerte resaca y no recuerdas cómo llegaste aquí.")
print_pause("Ves una espada vieja y oxidada apoyada contra la pared.")
choice = input("¿Quieres tomar la espada? (S/N): ").upper()

# Object
if choice == "S":
    has_sword = True
    print_pause("Tomas la espada. Se siente pesada y mal balanceada, pero es mejor que nada.")

else:
    print_pause("Decides no tomar la espada. Esperemos que no te arrepientas...")

print_pause("Caminas por un pasillo largo y oscuro.")
print_pause("Llegas a una bifurcación. El pasillo se divide en dos caminos oscuros.")
print_pause("El de la izquierda huele a algo vagamente metálico. El de la derecha tiene un ligero aroma a papel viejo y polvo.")
choice = input("¿Qué camino tomas? (A = izquierda, B = derecha): ").upper()

if choice == "A":
    print_pause("Te adentras en el pasillo de la izquierda. El aire es extrañamente húmedo y del techo gotea una sustancia pegajosa.")
    print_pause("De repente, una forma oscura y amorfa se desprende del techo sobre ti.")
    print_pause("Antes de que puedas reaccionar, te envuelve por completo, y tu aventura termina en la asfixiante oscuridad.")
    print_pause("Fin del juego.")
    exit()

else:
    print_pause("Eliges el camino de la derecha y llegas a una sala circular.")
    print_pause("Estanterías repletas de libros polvorientos cubren las paredes del suelo al techo. Es una biblioteca.")
    print_pause("En el fondo de la sala hay un atril de piedra con un libro abierto. En una estantería, un libro de color rojo intenso parece fuera de lugar.")
    choice = input("¿Qué quieres investigar? (A = atril, B = libro rojo): ").upper()

    if choice == "A":
        secret_num = random.randint(1,1000)
        aux_num = random.randint(1, 20)
        result_num = 2 * secret_num + aux_num

        print_pause("Te acercas al atril. Detrás del atril, una puerta de madera bloquea el camino.")
        print_pause("Al acercarte, el texto del libro se ilumina. Dice:")
        print_pause("\"Aquel que desee cruzar esta puerta, deberá resolver el enigma. "
                    "Dobla el valor secreto, súmale {} y obtenrás {}.\"".format(aux_num, result_num))
        secret_choice = int(input("¿Cuál es el valor secreto?: "))
        if secret_choice == secret_num:
            print_pause("Con un crujido lento, la madera cede y la puerta se abre por sí sola.")
            print_pause("Has resuelto el enigma. El camino continúa.")
        else:
            has_wound = True
            print_pause("Las letras del libro se tornan rojas.")
            print_pause("De las paredes emergen ranuras, y una rafaga de flechas silba por el aire.")
            print_pause("Rapidamente te lanzas contra la puerta y esta cruje bajo tu peso, cediendo. Sin embargo una flecha te ha alcanzado y estás herido.")

        print_pause("Llegas en una armería abandonada. Hay armas rotas y armaduras oxidadas por todas partes.")
        print_pause("Ves una trampilla de madera en el suelo, pero algo más te llama la atención: un débil brillo metálico asoma por debajo de un montón de chatarra en una esquina.")
        choice = input("¿Qué haces? (A = ir a la trampilla, B = investigar brillo): ").upper()

        if choice == "A":
            print_pause("Ignoras el brillo y abres la trampilla. Un olor nauseabundo sube desde la oscuridad. Bajas por una escalera")
            print_pause("Aterrizas en una caverna apestosa. Un ogro gigante te ve y ruge, bloqueando el camino.")
            if not has_sword:
                print_pause("El ogro se abalanza sobre ti. Sin nada con qué defenderte, tu aventura llega a un final rápido y brutal.")
                print_pause("Fin del juego.")
                exit()
            elif has_sword and not has_wound:
                print_pause("La batalla es feroz, pero estás en plena forma. Esquivas su porra y contraatacas con precisión. Tras un combate épico, el gigante cae.")
                print_pause("Ves una escalera de mano al fondo de la cueva. Te sientes fuerte, podrías subir.")
                choice = input("¿Subes por la escalera o descansas un momento? (A = subir, B = descansar): ").upper()

                if choice == "A":
                    print_pause("Con la adrenalina a tope, subes la escalera. Llegas a una caverna aún más grande, el techo se pierde en la oscuridad.")
                    print_pause("Un ojo, más grande que tú, se abre en las sombras. Sientes un calor intenso.")
                    print_pause("Un dragón te encuentra y te incinera en un instante.")
                    print_pause("Fin del juego.")
                    exit()
                else:
                    print_pause("Decides recuperar el aliento. Mientras descansas, una pequeña criatura sale por un agujero en la pared que no habías visto")
                    print_pause("Te acercas al lugar por el que salió y descubres un estrecho tunel, el cual tomas.")
                    print_pause("Para tu sorpresa, sales al exterior. ¡Eres libre!")
                    print_pause("Fin del juego.")
                    exit()
            else:
                print_pause("Luchas valientemente, pero la herida del salón del acertijo te pasa factura.")
                print_pause("Logras derrotar al ogro, pero caes de rodillas, exhausto y sin fuerzas.")
                print_pause("Mientras descansas, una pequeña criatura sale por un agujero en la pared que no habías visto")
                print_pause("Te acercas al lugar por el que salió y descubres un estrecho tunel, el cual tomas.")
                print_pause("Para tu sorpresa, sales al exterior. ¡Eres libre!, aunque necesitas buscar ayuda urgentemente.")
                print_pause("Fin del juego.")
                exit()

        else:
            print_pause("Apartas un peto oxidado y descubres una vieja corona de hierro.")
            choice = input("¿Quieres ponerte la corona? (S/N): ").upper()
            if choice == "S" and has_sword:
                print_pause("Te pones la corona. Un poder oscuro fluye hacia ti. De pronto, la espada en tu mano comienza a brillar con la misma energía.")
                print_pause("El poder de la mazmorra es ahora tuyo. Eres la criatura más poderosa en toda la mazmorra, sin embargo no dejas de preguntarte si esto es realmente una victoria.")
                print_pause("Fin del juego.")
                exit()
            elif choice == "S"and has_sword == False:
                print_pause("Te pones la corona. Un poder oscuro fluye hacia ti, pero no tienes un ancla que lo dirija.")
                print_pause("Tu cuerpo se desvanece, transformándote en un espectro más en la mazmorra, condenado a una existencia etérea por toda la eternidad.")
                print_pause("Fin del juego.")
                exit()
            else:
                print_pause("Ignoras la corona y abres la trampilla. Un olor nauseabundo sube desde la oscuridad. Bajas por una escalera")
                print_pause("Aterrizas en una caverna apestosa. Un ogro gigante te ve y ruge, bloqueando el camino.")
                if not has_sword:
                    print_pause("El ogro se abalanza sobre ti. Sin nada con qué defenderte, tu aventura llega a un final rápido y brutal.")
                    print_pause("Fin del juego.")
                    exit()
                elif has_sword and not has_wound:
                    print_pause("La batalla es feroz, pero estás en plena forma. Esquivas su porra y contraatacas con precisión. Tras un combate épico, el gigante cae.")
                    print_pause("Ves una escalera de mano al fondo de la cueva. Te sientes fuerte, podrías subir.")
                    choice = input("¿Subes por la escalera o descansas un momento? (A = subir, B = descansar): ").upper()

                    if choice == "A":
                        print_pause("Con la adrenalina a tope, subes la escalera. Llegas a una caverna aún más grande, el techo se pierde en la oscuridad.")
                        print_pause("Un ojo, más grande que tú, se abre en las sombras. Sientes un calor intenso.")
                        print_pause("Un dragón te encuentra y te incinera en un instante.")
                        print_pause("Fin del juego.")
                        exit()
                    else:
                        print_pause("Decides recuperar el aliento. Mientras descansas, una pequeña criatura sale por un agujero en la pared que no habías visto")
                        print_pause("Te acercas al lugar por el que salió y descubres un estrecho tunel, el cual tomas.")
                        print_pause("Para tu sorpresa, sales al exterior. ¡Eres libre!")
                        print_pause("Fin del juego.")
                        exit()
                else:
                    print_pause("Luchas valientemente, pero la herida del salón del acertijo te pasa factura.")
                    print_pause("Logras derrotar al ogro, pero caes de rodillas, exhausto y sin fuerzas.")
                    print_pause("Mientras descansas, una pequeña criatura sale por un agujero en la pared que no habías visto")
                    print_pause("Te acercas al lugar por el que salió y descubres un estrecho tunel, el cual tomas.")
                    print_pause("Para tu sorpresa, sales al exterior. ¡Eres libre!, aunque necesitas buscar ayuda urgentemente.")
                    print_pause("Fin del juego.")
                    exit()
    else:
        print_pause("Tiras del libro rojo. La estantería se desliza, revelando un pasadizo secreto.")
        print_pause("El aire que sale de él es húmedo y huele a agua estancada y moho.")
        print_pause("Al tomar el pasadizo te lleva a una cripta inundada. El agua helada te llega a las rodillas.")
        print_pause("Mientras te adentras en la cripta un tentáculo viscoso emerge del agua turbia, te agarra y te arrastra hasta lo más profundo de la cripta.")
        print_pause("Fin del juego.")
        exit()
