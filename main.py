import tkinter as tk
from tkinter import ttk
import sys
from funciones import maximize_image
from datetime import datetime
import time, random
import threading
import queue

input_queue = queue.Queue()


start_button = None

def get_input(prompt):
    """Pide texto desde la consola GUI: muestra prompt y espera por la entrada del usuario."""
    print(prompt, end='')   
    return input_queue.get()  

class Personaje:
    def __init__(self,nombre,vida,ataque,defensa,):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa
        
class Skill:
    def __init__(self,nombre,atributo,dmg,ventaja = False,objetivo = None):
        self.nombre = nombre
        self.atributo = atributo
        self.dmg = dmg
        self.ventaja = ventaja
        self.objetivo = objetivo
    def tabla_elemental(self):
        if self.atributo == "fuego" and self.objetivo.atributo == "planta":
            self.ventaja = True
        elif self.atributo == "planta" and self.objetivo.atributo == "agua":
            self.ventaja = True
        elif self.atributo == "agua" and self.objetivo.atributo == "fuego":
            self.ventaja = True
    def dmg_system(self):
        if self.ventaja == True:
            return (self.dmg * 2) - (self.objetivo.defensa * 0.5)
        else:
            return self.dmg - (self.objetivo.defensa * 0.5)

firesword = Skill("Firesword","fuego",20,objetivo=None)
watersword = Skill("Watersword","agua",20,objetivo=None)
earthsword = Skill("Earthsword","planta",20,objetivo=None)


class Personaje_principal(Personaje):
    def __init__(self,nombre,vida,ataque,defensa,):
        super().__init__(nombre,vida,ataque,defensa,)
    
    def atacar(self,objetivo,skill=None):
        global enemy_hurt
        if objetivo.vida > 0:
            choice = get_input("Elige una habilidad: \n"
                               "1. Firesword\n"
                               "2. Watersword\n"
                               "3. Earthsword\n").strip()
            try:
                skill = int(choice)
            except Exception:
                print("Entrada inválida. Se cancela el ataque.")
                return
            if skill == 1:
                skill = firesword
                firesword.objetivo = objetivo
                print("Has elegido Firesword\n"
                "-----------------------")
                time.sleep(1)
                firesword.tabla_elemental()
                if firesword.ventaja:
                    print("el ataque es super efectivo\n"
                        "-----------------------")
                    time.sleep(1)
                    objetivo.vida -= firesword.dmg_system()
                    print("el objetivo ha recibido", firesword.dmg_system(), "puntos de daño y ahora su vida es", objetivo.vida, "\n"
                          "-----------------------")
                    enemy_hurt = True
                    time.sleep(1)
                elif not firesword.ventaja:
                    objetivo.vida -= firesword.dmg_system()
                print("el objetivo ha recibido", firesword.dmg_system(), "puntos de daño y ahora su vida es", objetivo.vida, "\n"
                          "-----------------------")
                enemy_hurt = True
                time.sleep(1)
                
            elif skill == 2:
                skill = watersword
                watersword.objetivo = objetivo
                print("Has elegido Watersword\n"
                "-----------------------")
                watersword.tabla_elemental()
                time.sleep(1)
                if watersword.ventaja:
                    print("el ataque es super efectivo\n"
                        "-----------------------")
                    time.sleep(1)
                    objetivo.vida -= watersword.dmg_system()
                    print("el objetivo ha recibido", watersword.dmg_system(), "puntos de daño y ahora su vida es", objetivo.vida, "\n"
                          "-----------------------")
                    enemy_hurt = True
                    time.sleep(1)
                elif not watersword.ventaja:
                    objetivo.vida -= watersword.dmg_system()
                    print("el objetivo ha recibido", watersword.dmg_system(), "puntos de daño y ahora su vida es", objetivo.vida, "\n"
                            "-----------------------")
                    enemy_hurt = True
                time.sleep(1)
            elif skill == 3:
                skill = earthsword
                earthsword.objetivo = objetivo
                print("Has elegido Earthsword\n"
                "-----------------------")
                earthsword.tabla_elemental()
                time.sleep(1)
                if earthsword.ventaja:
                    print("el ataque es super efectivo\n"
                        "-----------------------")
                    time.sleep(1)
                    objetivo.vida -= earthsword.dmg_system()
                    print("el objetivo ha recibido", earthsword.dmg_system(), "puntos de daño y ahora su vida es", objetivo.vida, "\n"
                            "-----------------------")
                    enemy_hurt = True
                    time.sleep(1)
                elif not earthsword.ventaja:
                    objetivo.vida -= earthsword.dmg_system()
                    print("el objetivo ha recibido", earthsword.dmg_system(), "puntos de daño y ahora su vida es", objetivo.vida, "\n"
                            "-----------------------")
                    enemy_hurt = True
                time.sleep(1)
        
            else:
                print("Has ganado el combate")

    def curar(self):
        self.vida += 10
        print("Has curado 10 puntos de vida. Tu vida actual es:", self.vida, "\n"
              "-----------------------")
        time.sleep(1)
    
class Enemigo(Personaje):
    def __init__(self,nombre,vida,ataque,defensa,atributo,):
        super().__init__(nombre,vida,ataque,defensa,)
        self.atributo = atributo
    def atacar(self,objetivo):
        global player_hurt
        if objetivo.vida > 0:
            dmg = self.ataque - objetivo.defensa * 0.5
            if dmg < 0:
                print("El ataque no hace daño.")
            else:
                objetivo.vida -= dmg
                print(self.nombre, "ha atacado a", objetivo.nombre, "\n"
                      "-----------------------")
                
                time.sleep(1)
                print( objetivo.nombre, "ha recibido",dmg, "puntos de daño. Su vida actual es", objetivo.vida, "\n"
                      "-----------------------")
                player_hurt = True
                time.sleep(1)
        elif objetivo.vida <= 0:
            print("Haz perdido el combate")


name = None
player = Personaje_principal(name, 100, 20, 10)
atributos = ["fuego", "agua", "planta"]
enemy = None

root = None
screen = None
frames = {}
console_text = None
console_input = None
status_label_widget = None
canvas_ref = None
image_refs = {}  
player_x_start_pos = 700
enemy_x_start_pos = 950
player_move = False
enemy_move = False
player_idle = True
enemy_idle = True
player_hurt = False
enemy_hurt = False
class ConsoleRedirector(object):
    """Redirige la salida de print() al widget de texto."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, st):
        if not st:
            return
        def append():
            try:
                # Si el widget está en "disabled" habilitamos temporalmente para insertar
                if str(self.text_widget.cget("state")) == "disabled":
                    self.text_widget.config(state="normal")
                    self.text_widget.insert(tk.END, str(st))
                    self.text_widget.config(state="disabled")
                else:
                    self.text_widget.insert(tk.END, str(st))
                self.text_widget.see(tk.END)
            except tk.TclError:
                pass
        try:
            self.text_widget.after(0, append)
        except Exception:
            append()

    def flush(self):
        pass
   



    #Crear una forma en la que presentar a varios eneemigos 
def combat():
    global player,enemy,enemy,atributos,player_move,player_idle,enemy_idle,enemy_move,t
    player.nombre = get_input("Escribe el nombre de tu personaje: ")
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
        if enemy.vida <= 0:
            print("¡Has derrotado al enemigo!")
            show_frame("End")
            break
      

        print("\nEs el turno del jugador\n----------------------")
        time.sleep(1)
        print(f"Enemigo: {enemy.nombre} ({enemy.atributo}) - Vida: {enemy.vida}\n")

        accion = get_input("Elige atacar 0 curar\n----------------------\n").lower()
        if accion == "atacar":
            print(f"Atacas a {enemy.nombre}\n----------------------")
            player.atacar(enemy)
            player_move = True
            time.sleep(1)

        elif accion == "curar":
            player.curar()
            time.sleep(1)
        else:
            print("Acción no válida.")
            continue

        #Turno del enemigo
        print("\nEs el turno del enemigo\n----------------------")
        time.sleep(1)
        if enemy.vida > 0:
            enemy.atacar(player)
            enemy_move = True
            if player.vida <= 0:
                print("Has perdido el combate")
                return
            time.sleep(1)

def show_frame(frame_name):
    """Muestra el frame solicitado."""
    global frames, enemy
    frame = frames[frame_name]
    frame.tkraise()
    if console_text:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Navegando a: {frame_name}")

    if frame_name == "Combat":
        enemy = None
        player.vida = 100

    elif frame_name == "Menu":
        # Resetear la consola (borrar texto y dejarla en modo disabled)
        try:
            console_text.config(state="normal")
            console_text.delete("1.0", tk.END)
            console_text.config(state="disabled")
        except Exception:
            pass

        # Vaciar la cola de inputs (seguro para hilos)
        try:
            with input_queue.mutex:
                input_queue.queue.clear()
        except Exception:
            # Fallback simple
            while not input_queue.empty():
                try:
                    input_queue.get_nowait()
                except Exception:
                    break

        # Rehabilitar el botón de inicio si existe
        try:
            if start_button:
                start_button.config(state="normal")
        except Exception:
            pass

def process_input(event=None):
    text = console_input.get().strip()
    console_input.delete(0, tk.END)
    if not text:
        return
    # insertar en la consola de solo-lectura habilitando temporalmente
    if console_text:
        if str(console_text.cget("state")) == "disabled":
            console_text.config(state="normal")
            console_text.insert(tk.END, f"\n> {text}\n")
            console_text.config(state="disabled")
        else:
            console_text.insert(tk.END, f"\n> {text}\n")
        console_text.see(tk.END)
    input_queue.put(text)

def create_menu(parent):
    global start_button
    menu = tk.Frame(parent)
    menu.grid(row=0, column=0, sticky="nsew")  
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    fondo = maximize_image("imagenes/menu.png", ancho_pantalla, alto_pantalla)
    canvas = tk.Canvas(menu, width=ancho_pantalla, height=alto_pantalla)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=fondo, anchor="nw")
    canvas.image = fondo  

    title = canvas.create_text(
            ancho_pantalla//2, 300,
            text="Combat Game",
            font =("times new roman", 200, "bold"),
            fill = "red")
    

    
    def start_game():
        global start_button
        if start_button:
            start_button.config(state="disabled")
        show_frame("Combat")
    start_button = tk.Button(
        menu,
        text="Start Game",
        font =("Times new roman", 20, "bold"),
        fg = "black",
        bg = "gray",
        command=start_game
    )
    start_button.config(width=15, height=2)
    canvas.create_window(
        ancho_pantalla//2, 800,
        window=start_button
    )
    test = tk.Button(
        menu,
        text="mmg",
        command = lambda :show_frame("End"))
    test.config(width=10, height=1, bg="blue", fg="white", font=("Arial", 12, "bold"))
    canvas.create_window(
    ancho_pantalla//2, 900,window = test
    )
    return menu

def create_combat(parent):
    global image_refs, player_state, enemy_state
    combat_frame = tk.Frame(parent)
    combat_frame.grid(row=0, column=0, sticky="nsew")  
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    
    fondo = maximize_image("imagenes/fondo.png", ancho_pantalla, alto_pantalla)   
    canvas = tk.Canvas(combat_frame, width=ancho_pantalla, height=alto_pantalla)
    canvas.pack(fill="both", expand=True) 
    canvas.create_image(0, 0, image=fondo, anchor="nw")
    
    
    image_refs['fondo'] = fondo
    canvas.image = fondo
    
    exit = tk.Button(combat_frame, text="Exit", command=lambda: show_frame("Menu"), )
    exit.config(width=10, height=1, bg="red", fg="white", font=("Arial", 12, "bold"))
    canvas.create_window(850, 50, anchor="nw", window=exit)

    
    start_fight = tk.Button(combat_frame, text="Start Fight",
                            command=lambda: threading.Thread(target=combat, daemon=True).start())
    start_fight.config(width=10, height=1, bg="green", fg="white", font=("Arial", 12, "bold"))
    canvas.create_window(700, 50, anchor="nw", window=start_fight)

    
    def return_to_idle():
        global player_move,player_idle, enemy_idle, enemy_move
        if  not player_move  and not player_idle :
            canvas.move(canvas.player_id, -140, 0)
            canvas.itemconfig(canvas.player_id, image=image_refs['player'])
            player_idle = True
        elif not enemy_move  and not enemy_idle :
            canvas.move(canvas.enemy_id, 140, 0)
            canvas.itemconfig(canvas.enemy_id, image=image_refs['enemy'])
            enemy_idle = True
    def animate_combatants():
        global player_move, enemy_move, player_idle, enemy_idle
        if player_move and  player_idle:               
                canvas.move(canvas.player_id, 140, 0)
                canvas.itemconfig(canvas.player_id, image=image_refs['playeratk1'])
                canvas.after(250, lambda: canvas.itemconfig(canvas.player_id, image=image_refs['playeratk']))
                player_move = False
                player_idle = False
        if enemy_move and  enemy_idle:
                canvas.move(canvas.enemy_id, -140, 0)
                canvas.itemconfig(canvas.enemy_id, image=image_refs['enemyatk1'])
                canvas.after(250, lambda: canvas.itemconfig(canvas.enemy_id, image=image_refs['enemyatk']))
                enemy_move = False
                enemy_idle = False   
    def animate_hurt():
        global player_hurt, enemy_hurt, player_idle, enemy_idle
        if player_hurt and player_idle:
            canvas.itemconfig(canvas.player_id, image=image_refs['playerhurt'])
            canvas.after(250, lambda: canvas.itemconfig(canvas.player_id, image=image_refs['player']))
            player_hurt = False
        if enemy_hurt and enemy_idle:
            canvas.itemconfig(canvas.enemy_id, image=image_refs['enemyhurt'])
            canvas.after(250, lambda: canvas.itemconfig(canvas.enemy_id, image=image_refs['enemy']))
            enemy_hurt = False


    def animate():
        animate_combatants()
        canvas.after(500, animate)
        canvas.after(700, animate_hurt)
        canvas.after(1500, return_to_idle)

    #Player imgs
    player_img = maximize_image("imagenes/player.png", 200, 200)   
    canvas.player_id = canvas.create_image(player_x_start_pos, 600, image=player_img, anchor="nw")
    image_refs['player'] = player_img

    playeratk = maximize_image("imagenes/playeratk.png", 200, 200)
    image_refs['playeratk'] = playeratk

    playeratk1 = maximize_image("imagenes/playeratk1.png", 200, 205)
    image_refs['playeratk1'] = playeratk1

    playerhurt = maximize_image("imagenes/playerhurt.png", 200, 200)
    image_refs['playerhurt'] = playerhurt
    #enemy imgs
    enemy_img = maximize_image("imagenes/enemy.png", 200, 200)
    canvas.enemy_id = canvas.create_image(enemy_x_start_pos, 600, image=enemy_img, anchor="nw")
    image_refs['enemy'] = enemy_img

    enemyatk = maximize_image("imagenes/enemyatk.png", 200, 200)
    image_refs['enemyatk'] = enemyatk

    enemyatk1 = maximize_image("imagenes/enemyatk1.png", 200, 200)
    image_refs['enemyatk1'] = enemyatk1

    enemyhurt = maximize_image("imagenes/enemyhurt.png", 200, 200)
    image_refs['enemyhurt'] = enemyhurt

     
    
   
    
    animate()
    return combat_frame

def create_end_frame(parent):
    end_frame = tk.Frame(parent)
    end_frame.grid(row=0, column=0, sticky="nsew")  
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    
    fondo = maximize_image("imagenes/end.png", ancho_pantalla, alto_pantalla)   
    canvas = tk.Canvas(end_frame, width=ancho_pantalla, height=alto_pantalla)
    canvas.pack(fill="both", expand=True) 
    canvas.create_image(0, 0, image=fondo, anchor="nw")
    
    # Guardar referencias para evitar que se borren
    image_refs['fondo'] = fondo
    canvas.image = fondo

    canvas.create_text(ancho_pantalla//2, 400,
        text="¡Has ganado el combate!",
        font =("Times new roman", 100, "bold"),
        fill = "white")
    
    exit = tk.Button(end_frame, text="Exit", command=lambda: show_frame("Menu"), )
    exit.config(width=10, height=1, bg="red", fg="white", font=("Arial", 12, "bold"))
    canvas.create_window((ancho_pantalla//2) - 50, 800, anchor="nw", window=exit)
    
    return end_frame
def setup_console_widget():
    global root, console_text, console_input
    
    # Frame contenedor negro
    console_frame = tk.Frame(root, bg="#0a0a0a")
    console_frame.grid(row=1, column=0, sticky="nsew")

    # Label de título (tk.Label para forzar fondo negro)
    tk.Label(console_frame, text="Consola de Sistema:", bg="#0a0a0a", fg="white", font=("Arial", 8)).pack(anchor="w", padx=5)

    # Widget de texto de salida
    console_text = tk.Text(console_frame, height=8, wrap="word", bg="#0a0a0a", fg="#00FF00", 
                           font=("Consolas", 10), insertbackground="white", bd=0)
    console_text.pack(fill="x", expand=True, padx=5)

    # poner la consola en modo lectura/deshabilitada para el usuario
    console_text.config(state="disabled")

    # Redirección
    sys.stdout = ConsoleRedirector(console_text)

    # Área de entrada
    input_frame = tk.Frame(console_frame, bg="#0a0a0a")
    input_frame.pack(fill="x", pady=5)

    console_input = tk.Entry(input_frame, bg="#222222", fg="white", font=("Consolas", 11),
                             insertbackground="white", bd=0)
    console_input.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    console_input.bind("<Return>", process_input)
    console_input.focus_set()

def start():
    global root, screen, frames
    root = tk.Tk()
    root.title("Combat Game")

   
    root.attributes("-fullscreen", True)   
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

   
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)
    root.columnconfigure(0, weight=1)

    # Contenedor principal
    screen = tk.Frame(root)
    screen.grid(row = 0, column = 0, sticky="nsew")
    screen.grid_rowconfigure(0, weight=1)
    screen.grid_columnconfigure(0, weight=1)

    setup_console_widget()

    frames["Menu"] = create_menu(screen)
    frames["Combat"] = create_combat(screen)
    frames["End"] = create_end_frame(screen)

    for frame in frames.values():
        frame.grid(row=0, column=0, sticky="nsew")
    
    show_frame("Menu")
    root.mainloop()


if __name__ == "__main__":
    start()








