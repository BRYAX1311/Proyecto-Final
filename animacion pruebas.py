import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=300, height=100, bg="green")
canvas.pack(pady=20)

# El texto dibujado en un Canvas es inherentemente 'transparente'
# respecto al fondo del propio Canvas.
canvas.create_text(
    150, 50,  # Coordenadas centrales
    text="Texto en Canvas",
    fill="yellow",
    font=('Helvetica', 20, 'bold')
)

root.mainloop()