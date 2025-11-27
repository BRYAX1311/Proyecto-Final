import tkinter as tk
from tkinter import ttk
import sys
from combate import combat
from funciones import maximize_image
from datetime import datetime


root = None
screen = None
frames = {}
console_text = None
console_input = None
status_label_widget = None
canvas_ref = None
image_refs = {}  # Agregar al inicio para guardar referencias


class ConsoleRedirector(object):
    """Redirige la salida de print() al widget de texto."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, st):
        self.text_widget.insert(tk.END, st)
        self.text_widget.see(tk.END) 

    def flush(self):
        pass

def show_frame(frame_name):
    """Muestra el frame solicitado."""
    global frames
    frame = frames[frame_name]
    frame.tkraise()
    if console_text:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Navegando a: {frame_name}")

def create_menu(parent):
    menu = tk.Frame(parent)
    menu.grid(row=0, column=0, sticky="nsew")  
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    fondo_tk = maximize_image("imagenes/menu.png", ancho_pantalla, alto_pantalla)
    label_fondo = (tk.Label(menu, image=fondo_tk))
    label_fondo.image = fondo_tk
    label_fondo.grid(row=0, column=0, sticky="nsew")
    start_button = ttk.Button(
        menu,
        text="Iniciar Combate",
        command=lambda: show_frame("Combat")
    )
    start_button.place(x=ancho_pantalla//2 - 100, y=alto_pantalla - 150, width=200, height=50)
    return menu

def create_combat(parent):
    global image_refs
    combat_frame = tk.Frame(parent)
    combat_frame.grid(row=0, column=0, sticky="nsew")  
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    
    fondo = maximize_image("imagenes/fondo.png", ancho_pantalla, alto_pantalla)   
    canvas = tk.Canvas(combat_frame, width=ancho_pantalla, height=alto_pantalla)
    canvas.pack(fill="both", expand=True) 
    canvas.create_image(0, 0, image=fondo, anchor="nw")
    
    # Guardar referencias para evitar que se borren
    image_refs['fondo'] = fondo
    canvas.image = fondo
    
    exit = tk.Button(combat_frame, text="Exit", command=lambda: show_frame("Menu"))
    exit.config(width=10, height=1, bg="red", fg="white", font=("Arial", 12, "bold"))
    canvas.create_window(850, 50, anchor="nw", window=exit)
        
    player_img = maximize_image("imagenes/player.png", 100, 100)
    canvas.create_image(300,320, image=player_img, anchor="nw")
    image_refs['player'] = player_img
    canvas.player = player_img

    enemy_img = maximize_image("imagenes/enemy.png", 100, 100)
    canvas.create_image(500,320, image=enemy_img, anchor="nw")
    image_refs['enemy'] = enemy_img
    canvas.enemy = enemy_img

    return combat_frame
def start():
    global root, screen, frames
    root = tk.Tk()
    root.title("Combat Game")
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")

    # Contenedor principal
    screen = tk.Frame(root)
    screen.pack(side="top", fill="both", expand=True)
    screen.grid_rowconfigure(0, weight=1)
    screen.grid_columnconfigure(0, weight=1)

    frames["Menu"] = create_menu(screen)
    frames["Combat"] = create_combat(screen)

    for frame in frames.values():
        frame.grid(row=0, column=0, sticky="nsew")
    
    show_frame("Menu")
    root.mainloop()


if __name__ == "__main__":
    start()








