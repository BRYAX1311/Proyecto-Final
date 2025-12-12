import random,time
from clases import Personaje,Personaje_principal, Enemigo


name = input("introduce el nombre de tu personaje: ")
player = Personaje_principal(name, 100, 20, 10)
atributos = ["fuego", "agua", "planta"]
enemy = None


def combat():
    global player, enemy, atributos 
    
    # Crear un ÚNICO enemigo
    nombre_enemigo = "Orc"
    enemy = Enemigo(
        nombre_enemigo,
        random.randint(80, 120),
        random.randint(5, 15),
        random.randint(1, 5),
        random.choice(atributos))
    
    print("El combate ha iniciado\n"
        "----------------------")
    time.sleep(1)
    print(f"Enemigo: {enemy.nombre} ({enemy.atributo}) - Vida: {enemy.vida}\n")

    while True:
        # Verificar si el enemigo sigue vivo
        if enemy.vida <= 0:
            print("¡Has derrotado al enemigo!")
            break

        print("\nEs el turno del jugador\n----------------------")
        time.sleep(1)
        print(f"Enemigo: {enemy.nombre} ({enemy.atributo}) - Vida: {enemy.vida}\n")

        accion = int(input("Elige\n"
                        "1.atacar\n"
                        "2.curar \n----------------------\n"))
        if accion == 1:
            print(f"Atacas a {enemy.nombre}\n----------------------")
            player.atacar(enemy)
            
        elif accion == 2:
            player.curar()
            time.sleep(1)
        else:
            print("Acción no válida.")
            continue

        # Turno del enemigo
        print("\nEs el turno del enemigo\n----------------------")
        time.sleep(1)
        if enemy.vida > 0:
            enemy.atacar(player)
            if player.vida <= 0:
                print("Has perdido el combate")
                return
            time.sleep(1)

combat()











































































