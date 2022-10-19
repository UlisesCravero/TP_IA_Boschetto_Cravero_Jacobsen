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

        #((Xpj,Ypj), ListaCajas)
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
    # pared vertical izquierda
    (0,0),
    (0,1),
    (0,2),
    (0,3),    
    # pared horizontal arriba    
    (1,0),
    (2,0),
    (3,0),
    (4,0),

    (0,4),
    (1,4),
    (1,5),

    (2,5),
    (3,5),
    (4,5),    

    (4,1),
    (4,2),
    (4,3),
    (4,4),
    

)

def calcularAdy(x,y,accion):
        if accion == "izquierda":
            return (x+1,y)
        if accion == "derecha":
            return (x-1,y)
        if accion == "arriba":
            return (x, y-1)
        if accion == "abajo":
            return (x, y+1)

class Sokoban(SearchProblem):

    

    def actions(self, state):
        acciones_disponibles = []
        # las acciones son 4: arriba, abajo, izuquierda, derecha
       
        pos_pj, cajas = state
        x_pj, y_pj = pos_pj
        adyacentes = [
            ((x_pj, y_pj + 1), "abajo"),
            ((x_pj, y_pj - 1),"arriba"), 
            ((x_pj + 1, y_pj), "derecha"),
            ((x_pj - 1, y_pj), "izquierda")
        ]


        for (destino, direccion) in adyacentes:
            #if direccion == "izquierda":
            x, y = destino
            ady_caja = calcularAdy(x,y,direccion)
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
        x_pj, y_pj = pos_pj 
        accion, tipo = action
        destino = calcularAdy(x_pj,y_pj, accion)
        if tipo == "mov":
            return (destino, cajas)
        if tipo == "caja":
            x_des_pj, y_des_pj = destino
            destino_caja = calcularAdy(x_des_pj,y_des_pj, accion)
            #mover caja
            cajas_modificadas = cajas #FALTA MOVER LA CAJA EN ESTO
            return (destino,cajas_modificadas)


    def cost(self, state1, action, state2):
        
        return ...
        

    def is_goal(self, state):
        hab_bombero, hab_restante = state
        return ...


    def heuristic(self, state):
        
        heuristica = 0 
        return heuristica

        



if __name__ == "__main__":
    viewer = BaseViewer()
    #result = depth_first(MisionerosProblem(INICIAL), graph_search=True, viewer=viewer)
    #result = breadth_first(MisionerosProblem(INICIAL), graph_search=True, viewer=viewer)
    result = astar(Sokoban(INITIAL), viewer=viewer)

    for action, state in result.path():
        print("Haciendo", action, "llegué a:")
        print(state)

    print("Profundidad:", len(list(result.path())))
    print("Stats:")
    print(viewer.stats)
