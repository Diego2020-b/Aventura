import os
import random
import helpers
import time

def juego(jugador1, jugador2, tablero, turno=0):
    os.system('cls')
    option = None
    num_dado = 0
    N = len(tablero)
    M = len(tablero[0])

    while True:
        helpers.imprimir_tablero(tablero, jug1, jug2)
        jug = jug1 if turno % 2 == 0 else jug2

        print("Turno del jugador {}".format(jug["nombre"]))
        if jug["tipo"] == "humano":
            option = helpers.mostrar_menu({"1": "Lanzar el dado", "2": "Guardar partida y salir", "3": "Salir"}, " ")
            if option == 3:
                break
            if option == 2:
                helpers.guardar_juego(jug1, jug2, tablero, turno)
                break
            if option == 1:
                num_dado = random.randint(1,6)
        else:        
            num_dado = random.randint(1,6)
            print("Maquina pensando...")
            time.sleep(1.5)
        
        helpers.mover_jugador(tablero, jug, num_dado, N, M)
        os.system('cls')
        print("El dado es: " + str(num_dado))
        print(f'Puntaje {jug1["nombre"]}: {jug1["puntos"]}')
        print(f'Puntaje {jug2["nombre"]}: {jug2["puntos"]}')

        if (jug['position']['x']==0 and jug['position']['y'] >=M-1):
            helpers.imprimir_tablero(tablero, jug1, jug2)
            print("Juego termniado")
            print("El ganador es {}".format(jug["nombre"]))
            print(f'Puntaje {jug1["nombre"]}: {jug1["puntos"]}')
            print(f'Puntaje {jug2["nombre"]}: {jug2["puntos"]}')
            input("Presione enter para regresar al menu: ")
            break
        turno+=1
        

jug1 = {
    'nombre': '',
    'puntos': 0,
    'position': {
        'x': 0,
        'y': 0
    },
    'tipo': 'maquina'
}

jug2 = {
    'nombre': 'computadora',
    'puntos': 0,
    'position': {
        'x': 0,
        'y': 0
    },
    'tipo': 'maquina'
}

while True:
    os.system('cls')
    print("Aventura")
    print("---------------------")
    menu = {
        "1": ("Para un jugador"),
        "2": ("Dos jugadores"),
        "3": ("Cargar Partida"),
        "4": ("Salir")
    }
    option = helpers.mostrar_menu(menu)
    if (option==4):
        break

    if (option == 3):
        jug1, jug2, tablero, turno = helpers.cargar_juego()
        juego(jug1, jug2, tablero, turno)

    if option==1 or option==2:
        cantidad_jugadores=option

        if cantidad_jugadores == 1:
            jug1['nombre'] = input("Ingrese nombre: ")
        
        dimension = input("Ingrese tamaño del tablero (N,M): ")
        partes = dimension.split(',')
        N = int(partes[0])
        M = int(partes[1])
        tablero = helpers.generar_tablero(N, M)

        if cantidad_jugadores == 1:
            jug1['tipo'] = 'humano'
            jug1['position']['x'] = N - 1
            jug2['position']['x'] = N - 1
        if cantidad_jugadores == 2:
            jug1['nombre'] = input("Ingrese nombre jugador 1: ")
            jug1['tipo'] = 'humano'
            jug1['position']['x'] = N - 1
            jug2['position']['x'] = N - 1
            jug2['nombre'] = input("Ingrese nombre jugador 2: ")
            jug2['tipo'] = 'humano'

        juego(jug1, jug2, tablero)
print("Good Bye Cowboy")
