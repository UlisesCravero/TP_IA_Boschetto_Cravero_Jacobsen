from itertools import combinations

from simpleai.search import CspProblem, backtrack

def armar_mapa(self, filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    return (filas, columnas,cantidad_paredes,cantidad_cajas_objetivos)

mapa_resultante =  armar_mapa(5,4,3,2)

problem_variables = []
CAJAS = []
OBJETIVOS = []
PAREDES = []



for pared in mapa_resultante[2]:
    #problem_variables.append("pared{}").format(pared+1)
    PAREDES.append("pared{}").format(pared+1)

for caja_obj in mapa_resultante[2]:
    CAJAS.append("caja{}").format(caja_obj+1)
    OBJETIVOS.append("objetivo{}").format(caja_obj+1)

problem_variables = PAREDES + OBJETIVOS + CAJAS + "PJ"

domains = {}

columnas = list(range(mapa_resultante[1]))
filas = list(range(mapa_resultante[0]))

casilleros = [
    (row, col)
    for fil in filas
    for col in columnas
]


for variable in problem_variables:
    domains[variable] = casilleros


constraints = []

def different(variables, values):
    celda1, celda2 = values
    return celda1 != celda2


    
# las cajas, paredes y pj no pueden estar en el mismo lugar
PJ_CAJAS_PAREDES = "PJ" + CAJAS + PAREDES
for celda1, celda2 in combinations(PJ_CAJAS_PAREDES,2):
    constraints.append(((celda1, celda2), different))



# restriccion global para mirar que no todas las cajas esten en los objetivos

# TODO 2:
# agregar todas las restricciones de que sean diferentes las celdas dentro de cada mega-cuadrado (de 3x3)

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem)

print("Solution:")
print(solution)