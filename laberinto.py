import time
from combate import combat

def nivel_1():
    global nivel 
    habitaciones = {
        'comienzo': {'habitaciones': ['1'], 'items':[], "enemigos": []},
        '1': {'habitaciones': ['comienzo', '2', '3'], 'items':[],'enemigos': []},
        '2': {'habitaciones': ['1'], 'items':['llave'],"enemigos": []},
        '3': {'habitaciones': ['1', '4'], 'items':[], "enemigos": ['si']},
        '4': {'habitaciones': ['3', '5'], 'items': [], "enemigos": []},
        '5': {'habitaciones': ['4', 'salida'], 'items':[], "enemigos": ['si']}
    }
    habitacion = "comienzo"
    key = False
    while True:
        time.sleep(1)
        print("======================")
        print("estas en la habitacion",habitacion)
        for habitacion_cercana in habitaciones[habitacion]['habitaciones']:
            print('Puedes ir a la habitación más cercana', habitacion_cercana)
        nueva_habitacion = input("a que habitacion quieres ir?")
        if nueva_habitacion not in habitaciones[habitacion]["habitaciones"]:
            print("la habitacion no existe")
            time.sleep(2)
            continue 
        if nueva_habitacion == "salida" and not key:
            print("te falta la llave")
            time.sleep(2)
            continue 
        if nueva_habitacion == "salida":
            print("has pasado al nivel 2")
            break 
        habitacion = nueva_habitacion
        if 'llave' in habitaciones[habitacion]["items"]:
            key = True
            print("has encontrado la llave")
            habitaciones[habitacion]['items'].remove('llave')
        
        if 'si' in habitaciones[habitacion]["enemigos"]:
            combat()
            habitaciones[habitacion]['items'].remove('si')

nivel_1()