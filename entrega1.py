from logging import exception
from typing import Tuple
from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
    astar,
    greedy,
)
from simpleai.search.viewers import WebViewer, BaseViewer


        #((fila_pj,columna_pj), ListaCajas, cantidad_movimientos)
# inicio_Jugador = (1,1)
          #pos jugador     pos cajas
# INITIAL = ((1,1), ((2,2),(2,3)), 10)


OBJETIVOS = [
    (1,1),
    (1,5)
]
pj_inicial = (2,3)
cajas = [(1,2),(1,4)]
#PAREDES
PAREDES = [
    (0,0),
    (0,1),
    (0,2),
    (0,3),
    (0,4),
    (0,5),
    (0,6),

    (1,0),
    (1,6),

    (2,0),
    (2,6),

    (3,0),
    (3,1),
    (3,2),
    (3,3),
    (3,4),
    (3,5),
    (3,6),
] 



#una función jugar que recibirá como parámetros el mapa (paredes), 
# las posiciones actuales de las cajas y el jugador, las posiciones objetivos,
#  y la cantidad máxima de movimientos

def jugar( paredes,cajas,objetivos, jugador,maximos_movimientos):
            #todas las posiciones respetan (fila,columna)
            #tuplca con la posición del jugar, array de tuplas con pusición de las cajas, cantidad máxima de movimientos
    INITIAL = (jugador, tuple(tuple(caja) for caja in cajas),maximos_movimientos)
    
    # cambiar para no hacer esta asignación
    OBJETIVOS = tuple(tuple(obj) for obj in objetivos)
    PAREDES = tuple(tuple(pared) for pared in paredes)
    
    #secuencia de movimientos
    secuencia_movimientos = []

    pasos = astar(Sokoban(INITIAL))
    for accion, estado in pasos.path():
        if accion is not None:
            secuencia_movimientos.append(accion[2])
            #print("Action:", accion[2], "Cajas:", estado[1])
    
    return secuencia_movimientos

def calcularAdy(fila,columna,accion):
        if accion == "izquierda":
            return (fila, columna-1)
        if accion == "derecha":
            return (fila, columna+1)
        if accion == "arriba":
            return (fila-1,columna)
        if accion == "abajo":
            return (fila+1,columna)

class Sokoban(SearchProblem):

    def actions(self, state):
        acciones_disponibles = []
        # estructura action = posicion_destino, tipo_movimiento, direccion
    
        pos_pj, cajas, _ = state
        fila_pj, col_pj = pos_pj
        adyacentes = [
            ((fila_pj, col_pj + 1), "derecha"),
            ((fila_pj, col_pj - 1),"izquierda"), 
            ((fila_pj + 1, col_pj), "abajo"),
            ((fila_pj - 1, col_pj), "arriba")
        ]

        for (destino, direccion) in adyacentes:
            #if direccion == "izquierda":
            fila, columna = destino
            ady_caja = calcularAdy(fila,columna,direccion)
            if destino not in PAREDES and destino not in cajas:
                #no hay ningún obstaculo, muevo
                acciones_disponibles.append((destino, "mov",direccion))
            elif destino not in PAREDES and destino in cajas:
                #si no es pared, hay una caja
                if ady_caja not in PAREDES and ady_caja not in cajas:
                    acciones_disponibles.append((destino, "caja",direccion))
                
        return acciones_disponibles
            

    def result(self, state, action):
        #accion: texto con la direccion
        # ejemplo "izquierda", "derecha"
        pos_pj, cajas, cant_mov = state
        fila_pj, col_pj = pos_pj 
        accion, tipo, direccion = action    


        movimientos_restantes = cant_mov-1
        destino = calcularAdy(fila_pj,col_pj,direccion)
        if cant_mov > 0:
            if tipo == "mov":
                return (destino, cajas, movimientos_restantes)
            if tipo == "caja":
                fila_des_pj, col_des_pj = destino
                destino_caja = calcularAdy(fila_des_pj,col_des_pj, direccion)
                cajas_modificadas = []
                for caja in cajas:
                    if caja == destino:
                        #debo mover la caja al destino
                        cajas_modificadas.append(destino_caja)
                    else:
                        cajas_modificadas.append(caja)
                return (destino ,tuple(cajas_modificadas), movimientos_restantes)
        else:
            raise Exception("Loser! Te quedaste sin movimientos")
            

    def cost(self, state1, action, state2):
        # costo 1 porque se intenta encontrar la solución en la menor cantidad de movimientos posibles
        return 1
        

    def is_goal(self, state):
        _, cajas, _ = state
        for caja in cajas:
            if caja not in OBJETIVOS:
                return False
        return True


    def heuristic(self, state):
        # cantidad de movimientos que le faltan a cada caja para
        # llegar al objetivo más cercano
        _ , cajas, _ = state
        heuristica = 0
        for caja in cajas:
            if caja not in OBJETIVOS:
                f_caja, c_caja = caja
                objetivo_cercano = []
                for (f_obj,c_obj) in OBJETIVOS:
                    objetivo_cercano.append(abs(f_caja - f_obj) + abs(c_caja - c_obj))
                heuristica += min(objetivo_cercano)
        return heuristica



#def jugar(self, paredes,posiciones_cajas, posicion_jugador, objetivos,cant_max_movimientos):
movimientos = jugar(PAREDES,cajas,pj_inicial,OBJETIVOS,20)

