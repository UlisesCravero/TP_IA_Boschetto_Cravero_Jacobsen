from itertools import combinations
from simpleai.search import CspProblem, backtrack

def armar_mapa( filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    
    #mapa_resultante =  armar_mapa(5,4,3,2)
    if filas != columnas:
        print("es rectangulo") #CAMBIAR

    problem_variables = []
    CAJAS = []
    OBJETIVOS = []
    PAREDES = []



    for pared in cantidad_paredes:
        #problem_variables.append("pared{}").format(pared+1)
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

    # Restriccion de mas de una pared adyacente

    # Restriccion de no ubicar cajas en esquinas







    # TODO 2:
    # agregar todas las restricciones de que sean diferentes las celdas dentro de cada mega-cuadrado (de 3x3)

    problem = CspProblem(problem_variables, domains, constraints)
    solution = backtrack(problem)

    #print("Solution:")
    #print(solution)