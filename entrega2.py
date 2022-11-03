from itertools import combinations
from simpleai.search import CspProblem, backtrack
import re

def armar_mapa( filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    
    #mapa_resultante =  armar_mapa(5,4,3,2)
    if filas != columnas:
        print("es rectangulo") #CAMBIAR

    problem_variables = []
    CAJAS = []
    OBJETIVOS = []
    PAREDES = []



    for pared in cantidad_paredes:
        PAREDES.append("pared{}").format(pared+1)

    #la cantidad de cajas y objetivos es la misma
    for caja_obj in cantidad_cajas_objetivos:
        CAJAS.append("caja{}").format(caja_obj+1)
        OBJETIVOS.append("objetivo{}").format(caja_obj+1)

    problem_variables = PAREDES + OBJETIVOS + CAJAS + "PJ"

    domains = {}

    lista_columnas = list(range(columnas))
    lista_filas = list(range(filas))

    casilleros = [
        (fil, col)
        for fil in lista_filas
        for col in lista_columnas
    ]


    for variable in problem_variables:
        domains[variable] = casilleros


    constraints = []

    def different(problem_variables, values):
        celda1, celda2 = values
        return celda1 != celda2
 
   
    # las cajas, paredes y pj no pueden estar en el mismo lugar
    PJ_CAJAS_PAREDES = "PJ" + CAJAS + PAREDES
    for celda1, celda2 in combinations(PJ_CAJAS_PAREDES,2):
        constraints.append(((celda1, celda2), different))

    # los objetivos no deben estar arriba de una una pared 
    OBJ_PAREDES = OBJETIVOS + PAREDES
    for celda1, celda2 in combinations(OBJ_PAREDES,2):
        constraints.append(((celda1, celda2), different))

    
    # Restriccion que el juego no esté ganado       
    def game_not_win(variables, values):     
        aux_cajas = []       
        aux_objs = []    
        cantidad_co = 0
        for vari in variables:
            # expresión regular para saber si es caja
            x = re.search("^caja[0-9]+", vari)
            if x:
                #es caja
                aux_cajas.append(vari)
            else:
                #es objetivo
                aux_objs.append(vari)
        
        cantidad_co = len(aux_cajas)
        contador_cajas_en_objetivos = 0
        for caja in aux_cajas:
            for objetivo in aux_objs:
                if values[caja] == values[objetivo]:
                    contador_cajas_en_objetivos += 1

        return cantidad_cajas_objetivos != cantidad_co  

    CAJAS_OBJETIVOS = CAJAS + OBJETIVOS
    constraints.append(CAJAS_OBJETIVOS, game_not_win)

    
    
    # Restriccion de mas de una pared adyacente
    def dos_paredes_adyacentes_caja(variables,values):
        caja, paredes = variables
        ady_caja = [
            (caja[0]+1,caja[1]), #abajo
            (caja[0]-1,caja[1]), #arriba
            (caja[0],caja[1]+1), #derecha
            (caja[0],caja[1]-1)  #izquierda
        ]
        movimientos = []
        for f,c in ady_caja:
            if f>=0 or f<filas or c>=0 or c<filas:
                movimientos.append((f,c))

        cont_paredes_ady = 0
        for mov in movimientos:
            if mov in paredes:
                cont_paredes_ady += 1
        
        if cont_paredes_ady >= 2:
            return False
        elif len(movimientos) < 4 and cont_paredes_ady >= 1:
            return False
        else:
            return True

    for caja in CAJAS:
        constraints.append((caja,PAREDES),dos_paredes_adyacentes_caja)

    # Restriccion de no ubicar cajas en esquinas
    for caja in CAJAS:
        domains[caja].remove((0,0))
        domains[caja].remove((0,columnas-1))
        domains[caja].remove((filas-1,0))
        domains[caja].remove((filas-1,columnas-1))







    # TODO 2:
    # agregar todas las restricciones de que sean diferentes las celdas dentro de cada mega-cuadrado (de 3x3)

    problem = CspProblem(problem_variables, domains, constraints)
    solution = backtrack(problem)

    #print("Solution:")
    #print(solution)