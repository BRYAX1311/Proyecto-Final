import tkinter as tk
from tkinter import ttk
import sys
from datetime import datetime

# --- 1. Variables Globales (Estado de la aplicación) ---
root = None
container = None
frames = {} 
console_text = None
console_input = None
turn_count = 0
status_label_widget = None
canvas_ref = None

# --- 2. Redirección de Consola ---
class ConsoleRedirector(object):
    """Redirige la salida de print() al widget de texto."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, st):
        self.text_widget.insert(tk.END, st)
        self.text_widget.see(tk.END) # Auto-scroll al final

    def flush(self):
        pass

# --- 3. Funciones de Navegación y Lógica ---

def show_frame(page_name):
    """Muestra el frame solicitado."""
    global frames
    frame = frames[page_name]
    frame.tkraise()
    # Solo imprimimos si la consola ya existe
    if console_text: 
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Navegando a: {page_name}")

def perform_action():
    """Simula una acción de combate."""
    global turn_count, status_label_widget, canvas_ref, root
    
    # Validación de seguridad
    if not canvas_ref:
        return

    turn_count += 1
    damage = turn_count * 5
    
    new_text = f"¡HÉROE ATACA! Daño: {damage} (Turno {turn_count})"
    status_label_widget.config(text=new_text, fg="lightcoral")
    
    # Animación simple
    canvas_ref.move("hero", 20, 0)
    root.after(150, lambda: canvas_ref.move("hero", -20, 0))

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Turno {turn_count}: Héroe inflige {damage} de daño.")

def process_command(event=None):
    """Procesa comandos de texto."""
    global console_input, console_text, root
    
    command = console_input.get().strip()
    console_input.delete(0, tk.END) 

    if not command:
        return

    console_text.insert(tk.END, f"\n> {command}\n")

    cmd_lower = command.lower()
    if cmd_lower == "help":
        print("Comandos: help, status, clear, exit")
    elif cmd_lower == "status":
        print(f"Turno actual: {turn_count}")
    elif cmd_lower == "clear":
        console_text.delete('1.0', tk.END)
    elif cmd_lower == "exit":
        print("Cerrando...")
        root.after(1000, root.quit)
    else:
        print(f"Comando '{command}' no reconocido.")
        
    console_text.see(tk.END)

# --- 4. Construcción de Vistas ---

def create_start_page(parent):
    """Pantalla de Inicio."""
    # Usamos tk.Frame para poder usar bg color fácilmente
    start_frame = tk.Frame(parent, bg="#ADD8E6") 
    
    start_frame.columnconfigure(0, weight=1)
    start_frame.rowconfigure(0, weight=1)

    # CORRECCIÓN: Quitamos 'padding="20"' (que da error en tk.Frame)
    # y usamos padx/pady en el grid.
    main_content = tk.Frame(start_frame, bg="#ADD8E6") 
    main_content.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)

    # Usamos tk.Label en lugar de ttk.Label para que el fondo coincida exactamente con el azul
    label = tk.Label(main_content, text="Simulador de Combate", font=("Arial", 24, "bold"), bg="#ADD8E6", fg="#333333")
    label.pack(pady=10)

    info_label = tk.Label(main_content, text="Presiona el botón para iniciar.", font=("Arial", 12), bg="#ADD8E6", fg="#333333")
    info_label.pack(pady=20)

    start_button = ttk.Button(
        main_content,
        text="Iniciar Combate",
        command=lambda: show_frame("CombatSimulationPage")
    )
    start_button.pack(pady=20, ipadx=10, ipady=5)
    
    return start_frame

def create_combat_page(parent):
    """Pantalla de Combate."""
    global status_label_widget, canvas_ref
    
    combat_frame = tk.Frame(parent, bg="#1E1E1E")
    
    combat_frame.columnconfigure(0, weight=1)
    combat_frame.rowconfigure(0, weight=1)
    
    # Canvas
    canvas = tk.Canvas(combat_frame, bg="#333333", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    canvas_ref = canvas 

    # Label incrustado
    status_label_widget = tk.Label(
        canvas, 
        text="Simulación lista. Ataca.",
        font=("Arial", 14, "bold"),
        bg="#333333", 
        fg="yellow"
    )

    canvas.create_window(400, 50, window=status_label_widget, anchor="center")

    # Elementos visuales (Enemigo y Héroe)
    # Ajusté coordenadas para que se vean bien en la ventana
    canvas.create_oval(550, 200, 650, 300, fill="red", outline="darkred", tags="enemy")
    canvas.create_text(600, 250, text="Enemigo", fill="white", font=("Arial", 12))
    
    canvas.create_rectangle(150, 200, 250, 300, fill="blue", outline="darkblue", tags="hero")
    canvas.create_text(200, 250, text="Héroe", fill="white", font=("Arial", 12))
    
    # Botonera inferior
    control_frame = tk.Frame(combat_frame, bg="#1E1E1E")
    control_frame.grid(row=1, column=0, pady=(0, 20)) 

    action_button = ttk.Button(control_frame, text="ATACAR", command=perform_action)
    action_button.pack(side="left", padx=10, ipadx=10, ipady=5)

    back_button = ttk.Button(control_frame, text="Volver", command=lambda: show_frame("StartPage"))
    back_button.pack(side="left", padx=10)
    
    return combat_frame

# --- 5. Configuración de Consola ---

def setup_console_widget():
    """Configura la consola con colores oscuros consistentes."""
    global root, console_text, console_input
    
    # Frame contenedor negro
    console_frame = tk.Frame(root, bg="#0a0a0a")
    console_frame.pack(side="bottom", fill="x")

    # Label de título (tk.Label para forzar fondo negro)
    tk.Label(console_frame, text="Consola de Sistema:", bg="#0a0a0a", fg="white", font=("Arial", 8)).pack(anchor="w", padx=5)

    # Widget de texto de salida
    console_text = tk.Text(console_frame, height=8, wrap="word", bg="#0a0a0a", fg="#00FF00", 
                           font=("Consolas", 10), insertbackground="white", bd=0)
    console_text.pack(fill="x", expand=True, padx=5)

    # Redirección
    sys.stdout = ConsoleRedirector(console_text)

    # Área de entrada
    input_frame = tk.Frame(console_frame, bg="#0a0a0a")
    input_frame.pack(fill="x", pady=5)

    tk.Label(input_frame, text=" >", font=("Consolas", 12, "bold"), fg="white", bg="#0a0a0a").pack(side="left")
    
    console_input = tk.Entry(input_frame, bg="#222222", fg="white", font=("Consolas", 11), 
                             insertbackground="white", bd=0)
    console_input.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    
    console_input.bind("<Return>", process_command)
    console_input.focus_set()

# --- 6. Ejecución ---

def run_app():
    global root, container, frames

    root = tk.Tk()
    root.title("Simulador RPG (Procedural corregido)")
    root.geometry("800x600")

    # Contenedor principal
    container = tk.Frame(root)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    # Configurar consola antes de crear vistas (para capturar prints de creación)
    setup_console_widget()

    frames["StartPage"] = create_start_page(container)
    frames["CombatSimulationPage"] = create_combat_page(container)

    # Apilar frames
    for frame in frames.values():
        frame.grid(row=0, column=0, sticky="nsew")

    show_frame("StartPage")
    
    print("Sistema inicializado correctamente.")
    root.mainloop()

if __name__ == "__main__":
    run_app()
