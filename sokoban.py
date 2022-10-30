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

        #((fila_pj,columna_pj), ListaCajas)
inicio_Jugador = (1,1)
          #pos jugador     pos cajas
INITIAL = ((1,1), ((2,2),(2,3)))

Movimientos = [
  "arriba",
  "abajo",
  "derecha",
  "izquierda"
]

Objetivos = (
    (1,2),
    (2,4)
)
Paredes = (
    (0,0),
    (1,0),
    (2,0),
    (3,0),   
    (0,1),
    (0,2),
    (0,3),
    (0,4),
    (4,0),
    (4,1),
    (5,1),
    (5,2),
    (5,3),
    (5,4),    
    (1,4),
    (2,4),
    (3,4),
    (4,4),
)

#una función jugar que recibirá como parámetros el mapa (paredes), 
# las posiciones actuales de las cajas y el jugador, las posiciones objetivos,
#  y la cantidad máxima de movimientos

def jugar(self, paredes,posiciones_cajas, posicion_jugador, objetivos,cant_max_movimientos):
    return ...



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
        # las acciones son 4: arriba, abajo, izuquierda, derecha
       
        pos_pj, cajas = state
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
                acciones_disponibles.append(direccion, "mov")
            elif destino not in Paredes and destino in cajas:
                #si no es pared, hay una caja
                if ady_caja not in Paredes and ady_caja not in cajas:
                    acciones_disponibles.append(direccion, "caja")
                
        return acciones_disponibles
            

    def result(self, state, action):
        #accion: texto con la direccion
        # ejemplo "izquierda", "derecha"

        pos_pj, cajas = state
        fila_pj, col_pj = pos_pj 
        accion, tipo = action
        destino = calcularAdy(fila_pj,col_pj, accion)
        if tipo == "mov":
            return tuple(destino, cajas)
        if tipo == "caja":
            fila_des_pj, col_des_pj = destino
            destino_caja = calcularAdy(fila_des_pj,col_des_pj, accion)
            cajas_modificadas = []
            for caja in cajas:
                if caja == destino:
                    #debo mover la caja al destino
                    cajas_modificadas.append(destino_caja)
                else:
                    cajas_modificadas.append(caja)
            return tuple(destino,tuple(cajas_modificadas))


    def cost(self, state1, action, state2):
        # costo 1 porque se intenta encontrar la solución en la menor cantidad de movimientos posibles
        return 1
        

    def is_goal(self, state):
        _, cajas = state
        for caja in cajas:
            if caja not in Objetivos:
                return False
        return True


    def heuristic(self, state):
        # cantidad de movimientos que le faltan a cada caja para
        # llegar al objetivo más cercano
        _ , cajas = state
        heuristica = 0
        for caja in cajas:
            if caja not in Objetivos:
                f_caja, c_caja = caja
                objetivo_cercano = []
                for (f_obj,c_obj) in Objetivos:
                    objetivo_cercano.append(abs(f_caja - f_obj) + abs(c_caja - c_obj))
                heuristica += min(objetivo_cercano)

        return heuristica

#viewer = WebViewer()
viewer = BaseViewer()
result = astar(Sokoban(INITIAL))

print("Estado meta:")
print(result.state)

for action, state in result.path():
    print("Haciendo", action, "llegué a:")
    print(state)

print("Profundidad:", len(list(result.path())))

print("Stats:")

print(viewer.stats)
# if __name__ == "__main__":
#     viewer = BaseViewer()
#     #result = depth_first(MisionerosProblem(INICIAL), graph_search=True, viewer=viewer)
#     #result = breadth_first(MisionerosProblem(INICIAL), graph_search=True, viewer=viewer)
#     result = astar(Sokoban(INITIAL)) # , viewer=viewer

#     for action, state in result.path():
#         print("Haciendo", action, "llegué a:")
#         print(state)

#     print("Profundidad:", len(list(result.path())))
#     print("Stats:")
#     print(viewer.stats)
