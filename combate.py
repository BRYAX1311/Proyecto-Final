import random,time
from clases import Personaje,Personaje_principal, Enemigo

if __name__ == "__main__":
    name = input("introduce el nombre de tu personaje: ")
    player = Personaje_principal(name, 100, 20, 10)
    atributos = ["fuego", "agua", "planta"]
    enemys = []
    enemy_names = ["goblin","rata","esqueleto"]



    #Crear una forma en la que presentar a varios eneemigos 
def combat():
    global player,enemy,enemys,enemy_names,atributos 
    enemy_number = random.randint(1, 3)
    for i in range(enemy_number):
        nombre_enemigo = random.choice(enemy_names) + f" #{i+1}"
        enemy = Enemigo(
        nombre_enemigo,
        random.randint(80, 120),
        random.randint(5, 15),
        random.randint(1, 5),
        random.choice(atributos))
        enemys.append(enemy)  
    print("El combate ha iniciado\n"
        "----------------------")
    time.sleep(1)
    print("Enemigos presentes:")
    for idx, enemy in enumerate(enemys):
        print(f"{idx+1}. {enemy.nombre} ({enemy.atributo}) - Vida: {enemy.vida}")

    while True:
        
        vivos = [e for e in enemys if e.vida > 0]
        if not vivos:
            print("¡Has derrotado a todos los enemigos!")
            break

        print("\nEs el turno del jugador\n----------------------")
        time.sleep(1)
        print("Enemigos vivos:")
        for idx, enemy in enumerate(vivos):
            print(f"{idx+1}. {enemy.nombre} ({enemy.atributo}) - Vida: {enemy.vida}")

        accion = input("Elige atacar, curar, o salir\n----------------------\n").lower()
        if accion == "atacar":
            try:
                num = int(input("¿A qué enemigo quieres atacar? Escribe el número: "))
                objetivo = vivos[num-1]
            except (ValueError, IndexError):
                print("Número inválido.")
                continue
            print(f"Atacas a {objetivo.nombre}\n----------------------")
            player.atacar(objetivo)
            time.sleep(1)
        elif accion == "salir":
            print("Has salido del combate")
            break
        elif accion == "curar":
            player.curar()
            time.sleep(1)
        else:
            print("Acción no válida.")
            continue

            # Turno de los enemigos vivos
        print("\nEs el turno de los enemigos\n----------------------")
        time.sleep(1)
        for enemy in vivos:
            if enemy.vida > 0:
                enemy.atacar(player)
                if player.vida <= 0:
                    print("Has perdido el combate")
                    return
                time.sleep(1)











































































