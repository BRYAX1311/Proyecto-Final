import tkinter as tk
from PIL import Image, ImageTk
import os
def maximize_image(imagen, width, height):
    imag_pil = Image.open(imagen)
    imag_pil = imag_pil.resize((width, height), Image.LANCZOS)
    imag_tk = ImageTk.PhotoImage(imag_pil)
    return imag_tk
if __name__=="__main__":
    ventana = tk.Tk()
    ventana.title("Combat Game")
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")



    img_tk = maximize_image("imagenes/menu.png", ancho_pantalla, alto_pantalla)
    imagen = tk.Label(ventana, image=img_tk)
    imagen.image = img_tk  # mantener referencia para evitar que PIL Image sea recolectada
    imagen.pack(fill="both", expand=True)
    ventana.mainloop()














