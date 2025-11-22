import tkinter as tk
from PIL import Image, ImageTk

ventana = tk.Tk()
ventana.title("Combat Game")
ventana.geometry("1000x500")
mode = 0

class ConsoleRedirector(object):
    """Redirige la salida de print() al widget de texto."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, st):
        self.text_widget.insert(tk.END, st)
        self.text_widget.see(tk.END) # Auto-scroll al final

    def flush(self):
        pass

def mostrar_pantalla():
    global mode, canvas, fondo_tk, player_img, enemy_img
    
    # Limpiar canvas anterior
    for widget in ventana.winfo_children():
        widget.destroy()
    
    if mode == 0:
        fondo = Image.open("imagenes/menu.png")
        fondo = fondo.resize((1000,500))
        fondo_tk = ImageTk.PhotoImage(fondo)

        canvas = tk.Canvas(ventana, width=1000, height=500)
        canvas.pack(fill="both", expand=True)
        
        canvas.create_image(0, 0, image=fondo_tk, anchor="nw")
        
        button_start = tk.Button(ventana, text="Start Game", command=lambda: cambiar_modo(1))
        button_start.config(width=20, height=2, bg="grey", fg="black", font=("Arial", 16, "bold"))
        canvas.create_window(380, 400, anchor="nw", window=button_start)

    elif mode == 1:
        fondo = Image.open("imagenes/fondo.png")
        fondo = fondo.resize((1000,500))
        fondo_tk = ImageTk.PhotoImage(fondo)
        
        canvas = tk.Canvas(ventana, width=1000, height=500)
        canvas.pack(fill="both", expand=True) 
        canvas.create_image(0, 0, image=fondo_tk, anchor="nw")
        console_frame = tk.Frame(ventana)
        console_frame.pack(side="bottom", fill="x", expand=True)
        
        exit = tk.Button(ventana, text="Exit", command=lambda: cambiar_modo(0))
        exit.config(width=10, height=1, bg="red", fg="white", font=("Arial", 12, "bold"))
        canvas.create_window(850, 50, anchor="nw", window=exit)
        
        player_img = ImageTk.PhotoImage(Image.open("imagenes/player.png").resize((100,100)))
        canvas.create_image(300,320, image=player_img, anchor="nw")

        enemy_img = ImageTk.PhotoImage(Image.open("imagenes/enemy.png").resize((100,100)))
        canvas.create_image(500,320, image=enemy_img, anchor="nw")

def cambiar_modo(nuevo_modo):
    global mode
    mode = nuevo_modo
    mostrar_pantalla()

# Mostrar pantalla inicial
mostrar_pantalla()

ventana.mainloop()

