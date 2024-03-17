import random
import json

def generar_simbolos():
    simbolos = {
        '1': '*', # suma 5 puntos
        '2': '+', # avanza 6 casillas
        '3': '-' # retrocede 8 casillas
    }
    '''
    suma = simbolos['1']
    adelanto = simbolos['2']
    retroceso = simbolos['3']
    '''
    list_num_simbolos = []
    for i in simbolos:
        if i == '1':
            list_num_simbolos += [i]*2
        if i == '2':
            list_num_simbolos += [i]*3
        if i == '3':
            list_num_simbolos += [i]*5
    return list_num_simbolos

def generar_tablero(N, M):
    tablero = []
    contenido = 0
    simbolos = generar_simbolos()

    for i in range(N):
        fila = []
        for j in range(M):
            fila.append(contenido)
        tablero.append(fila)
    for j in simbolos:
        selector_fila = random.randint(0, len(tablero)-1)
        selector_columna = random.randint(0, len(tablero[selector_fila])-1)
        if not (selector_fila ==N-1 and selector_columna == 0):
            if j == '1':
                tablero[selector_fila][selector_columna] = 1
            elif j == '2':
                tablero[selector_fila][selector_columna] = 2
            elif j == '3':
                tablero[selector_fila][selector_columna] = 3
    return tablero

def mostrar_menu(menu, end="\n"):
    option = None

    while True:
        for opcion in menu:
            print(f' {opcion}) {menu[opcion]}{end}', end='')
        print("")
        option = input("Escoja una opción (" + ",".join(menu.keys())   + "): ")
        if (option.isnumeric() and option in menu.keys()):
            return int(option)
        
def guardar_juego(jug1, jug2, tablero, turno):
    f = open("guardado.json", "w")
    f.write(json.dumps({"jug1": jug1, "jug2": jug2, "tablero": tablero, "turno": turno}))
    f.close()

def cargar_juego():
    f = open("guardado.json", "r")
    data = json.loads(f.read())
    f.close()
    return (data["jug1"], data["jug2"], data["tablero"], data["turno"])

def imprimir_tablero(tablero, jug1, jug2):
    for posX, fila in enumerate(tablero):
        for posY, celda in enumerate(fila):
            contenido = ''

            if celda == 1:
                contenido = '*'
            if celda == 2:
                contenido = '+'
            if celda == 3:
                contenido = '-'
            if (posX == jug1['position']['x'] and posY == jug1['position']['y']):
                contenido = contenido + '1'
            if (posX == jug2['position']['x'] and posY == jug2['position']['y']):
                contenido = contenido + '2'

            contenido = contenido.ljust(3, ' ')        
            imprimir = f'[ {contenido} ]' #'[ ' + contenido ' ]', end='' 
            print(imprimir, end='')

        if ((len(fila) - 1 - posX) % 2 == 0):
            direccion="\u2190"
        else:
            direccion="\u2192"
        print(direccion)

def mover_adelante(jug, distancia, N, M):
    distancia_recorrida = 0
    posFila = jug['position']['x']
    posColumna = jug['position']['y']

    while distancia_recorrida<distancia:
        incremento_fila = 0 # subir: -1 igual: 0
        incremento_columna = 0 # derecha: 1 izquierda: -1

        direccion=''
        if ((N - 1 - posFila) % 2 == 0):
            direccion='derecha'
        else:
            direccion='izquierda'

        if (direccion=='derecha'):
            if(posColumna==M-1):
                incremento_fila=-1
                incremento_columna=0
            else:
                incremento_columna=1
                incremento_fila=0
        elif (direccion=='izquierda'):
            if(posColumna==0):
                incremento_fila=-1
                incremento_columna=0
            else:
                incremento_columna=-1
                incremento_fila=0

        posFila+=incremento_fila
        posColumna+=incremento_columna
        distancia_recorrida+=1
        if posColumna == M-1 and posFila==0:
            break

    jug['position']['x'] = posFila
    jug['position']['y'] = posColumna

def mover_atras(jug, distancia, N, M):
    distancia_recorrida = 0
    posFila = jug['position']['x']
    posColumna = jug['position']['y']

    while distancia_recorrida<distancia:
        incremento_fila = 0 # subir: -1 igual: 0
        incremento_columna = 0 # derecha: 1 izquierda: -1

        direccion=''
        if ((N - 1 - posFila) % 2 == 0):
            direccion='izquierda'
        else:
            direccion='derecha'

        if (direccion=='derecha'):
            if(posColumna==M-1):
                incremento_fila=1
                incremento_columna=0
            else:
                incremento_columna=1
                incremento_fila=0
        elif (direccion=='izquierda'):
            if(posColumna==0):
                incremento_fila=1
                incremento_columna=0
            else:
                incremento_columna=-1
                incremento_fila=0

        posFila+=incremento_fila
        posColumna+=incremento_columna
        distancia_recorrida+=1
        if posColumna == 0 and posFila == N -1:
            break
    jug['position']['x'] = posFila
    jug['position']['y'] = posColumna

def mover_jugador(tablero, jug, distancia, N, M):
    mover_adelante(jug, distancia, N, M)
    posX = jug['position']['x']
    posY = jug['position']['y']
    jug["puntos"] += distancia

    while (tablero[posX][posY]!=0):
        trampa = tablero[posX][posY]
        if (trampa == 1):
            jug["puntos"] += 5
            tablero[posX][posY] = 0
            break
        if (trampa == 2):
            jug["puntos"] += 6
            mover_adelante(jug, 6, N, M)
            tablero[posX][posY] = 0
        if (trampa == 3):
            mover_atras(jug, 8, N, M)
            tablero[posX][posY] = 0
        posX = jug['position']['x']
        posY = jug['position']['y']
