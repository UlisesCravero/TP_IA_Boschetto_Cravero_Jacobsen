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

from entrega2 import PAREDES

        #((fila_pj,columna_pj), ListaCajas, cantidad_movimientos)
# inicio_Jugador = (1,1)
          #pos jugador     pos cajas
# INITIAL = ((1,1), ((2,2),(2,3)), 10)

Movimientos = [
  "arriba",
  "abajo",
  "derecha",
  "izquierda"
]

Objetivos = [
    (1,2),
    (2,4)
]
# INICIAL = (
#     (2,2), #Posicion del personaje
#     ((2,3),(5,1)), #Cajas
#     0, #Movimientos
# )
pj_inicial = (2,2)
cajas = ((2,3),(5,1))
#Paredes
Paredes = (
    (0,2),
    (0,3),
    (0,4),
    (0,5),
    (0,6),
    (1,0),
    (1,1),
    (1,2),
    (1,6),
    (2,0),
    (2,6),
    (3,0),
    (3,1),
    (3,2),
    (3,6),
    (4,0),
    (4,2),
    (4,3),
    (4,6),
    (5,0),
    (5,2),
    (5,6),
    (5,7),
    (6,0),
    (6,7),
    (7,0),
    (7,7),
    (8,0),
    (8,1),
    (8,2),
    (8,3),
    (8,4),
    (8,5),
    (8,6),
    (8,7),
)    

# Paredes = (
#     (0,0),
#     (1,0),
#     (2,0),
#     (3,0),   
#     (0,1),
#     (0,2),
#     (0,3),
#     (0,4),
#     (4,0),
#     (4,1),
#     (5,1),
#     (5,2),
#     (5,3),
#     (5,4),    
#     (1,4),
#     (2,4),
#     (3,4),
#     (4,4),
# )

#una función jugar que recibirá como parámetros el mapa (paredes), 
# las posiciones actuales de las cajas y el jugador, las posiciones objetivos,
#  y la cantidad máxima de movimientos

def jugar(self, paredes,posiciones_cajas, posicion_jugador, objetivos,cant_max_movimientos):
            #todas las posiciones respetan (fila,columna)
            #tuplca con la posición del jugar, array de tuplas con pusición de las cajas, cantidad máxima de movimientos
    INITIAL = (posicion_jugador,posiciones_cajas,cant_max_movimientos)
    
    # cambiar para no hacer esta asignación
    Objetivos = objetivos
    Paredes = paredes
    
    #secuencia de movimientos
    secuencia_movimientos = []
    
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
            #print("action")
            #print(state)
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
                if destino not in Paredes and destino not in cajas:
                    #no hay ningún obstaculo, muevo
                    acciones_disponibles.append((destino, "mov",direccion))
                elif destino not in Paredes and destino in cajas:
                    #si no es pared, hay una caja
                    if ady_caja not in Paredes and ady_caja not in cajas:
                        acciones_disponibles.append((destino, "caja",direccion))
                    
            return acciones_disponibles
                

        def result(self, state, action):
            # print("result")
            # print(state)
            # print(action)
            #accion: texto con la direccion
            # ejemplo "izquierda", "derecha"
            pos_pj, cajas, cant_mov = state
            fila_pj, col_pj = pos_pj 
            accion, tipo, direccion = action    

            #sabiendo la acción puedo llenar el array de secuencia de movimientos
            secuencia_movimientos.append(direccion)

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
                print("SIN MOVIMIENTOS")

        def cost(self, state1, action, state2):
            print("cost")
            # costo 1 porque se intenta encontrar la solución en la menor cantidad de movimientos posibles
            return 1
            

        def is_goal(self, state):
            #print("goal")
            #print(state)
            _, cajas, _ = state
            for caja in cajas:
                if caja not in Objetivos:
                    return False
            return True


        def heuristic(self, state):
            #print("heuristic")
            #print(state)
            # cantidad de movimientos que le faltan a cada caja para
            # llegar al objetivo más cercano
            _ , cajas, _ = state
            heuristica = 0
            for caja in cajas:
                if caja not in Objetivos:
                    f_caja, c_caja = caja
                    objetivo_cercano = []
                    for (f_obj,c_obj) in Objetivos:
                        objetivo_cercano.append(abs(f_caja - f_obj) + abs(c_caja - c_obj))
                    heuristica += min(objetivo_cercano)
            posicion, cajas, movimientos = state
            # return len(set(cajas) - set(Objetivos))
            return heuristica


    #lo que devuelve la función jugar
    return secuencia_movimientos
#viewer = WebViewer()
# viewer = BaseViewer()
# result = astar(Sokoban(INITIAL), graph_search=False, viewer=viewer)

# print("Estado meta:")
# print(result.state)

# for action, state in result.path():
#     print("Haciendo", action, "llegué a:")
#     print(state)

# print("Profundidad:", len(list(result.path())))

# print("Stats:")

# print(viewer.stats)

if __name__ == "__main__":
    viewer = BaseViewer()
    #result = depth_first(MisionerosProblem(INICIAL), graph_search=True, viewer=viewer)
    #result = breadth_first(MisionerosProblem(INICIAL), graph_search=True, viewer=viewer)
    
    result = astar(jugar(Paredes,cajas,pj_inicial,Objetivos,5) , viewer=viewer)

    for action, state in result.path():
        print("Haciendo", action, "llegué a:")
        print(state)

    print("Profundidad:", len(list(result.path())))
    print("Stats:")
    print(viewer.stats)
