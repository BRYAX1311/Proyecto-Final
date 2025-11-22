import time
import speech_recognition as speech_recog

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
        
        if objetivo.vida > 0:
            skill = int(input("Elige una habilidad: \n"
                        "1. Firesword\n"
                        "2. Watersword\n"
                        "3. Earthsword\n"))
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
                    time.sleep(1)
                elif not firesword.ventaja:
                    objetivo.vida -= firesword.dmg_system()
                print("el objetivo ha recibido", firesword.dmg_system(), "puntos de daño y ahora su vida es", objetivo.vida, "\n"
                          "-----------------------")
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
                    time.sleep(1)
                elif not watersword.ventaja:
                    objetivo.vida -= watersword.dmg_system()
                    print("el objetivo ha recibido", watersword.dmg_system(), "puntos de daño y ahora su vida es", objetivo.vida, "\n"
                            "-----------------------")
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
                    time.sleep(1)
                elif not earthsword.ventaja:
                    objetivo.vida -= earthsword.dmg_system()
                    print("el objetivo ha recibido", earthsword.dmg_system(), "puntos de daño y ahora su vida es", objetivo.vida, "\n"
                            "-----------------------")
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
                time.sleep(1)
        elif objetivo.vida <= 0:
            print("Haz perdido el combate")







         