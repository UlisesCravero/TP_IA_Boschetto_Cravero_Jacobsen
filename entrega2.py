from itertools import combinations
from simpleai.search import MOST_CONSTRAINED_VARIABLE, CspProblem, backtrack,LEAST_CONSTRAINING_VALUE,HIGHEST_DEGREE_VARIABLE
import re

def armar_mapa( filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    #domains["fila"] = numero
    #mapa_resultante =  armar_mapa(5,4,3,2)
    #if filas != columnas: #son variables?
    #    print("es rectangulo") # hay que sumar filas y colmunas como variables y controlar que sean enteros positivos distintos?
   
    CAJAS = []
    OBJETIVOS = []
    PAREDES = []
    constraints = []
    domains = {}
    
    for pared in list(range(cantidad_paredes)):
        PAREDES.append("pared{}".format(pared+1))

    #la cantidad de cajas y objetivos es la misma
    for caja_obj in list(range(cantidad_cajas_objetivos)):
        CAJAS.append("caja{}".format(caja_obj+1))
        OBJETIVOS.append("objetivo{}".format(caja_obj+1))

    problem_variables = PAREDES + OBJETIVOS + CAJAS + ["PJ"]

    
    lista_columnas = list(range(columnas))
    lista_filas = list(range(filas))
    casilleros = [
        (fil, col)
        for fil in lista_filas
        for col in lista_columnas
    ]

    for variable in problem_variables:
        domains[variable] = list(casilleros)
 

    def different(problem_variables, values):
        celda1, celda2 = values
        return celda1 != celda2
   
    # las cajas, paredes y pj no pueden estar en el mismo lugar
    PJ_CAJAS_PAREDES = ["PJ"] + CAJAS + PAREDES

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
            for valor in values:
                # expresión regular para saber si es caja               
                if re.search("^caja[0-9]+", vari):
                    #es caja
                    aux_cajas.append(valor)
                elif re.search("^objetivo[0-9]+", vari):
                    #es objetivo
                    aux_objs.append(valor)
        
        for caja in aux_cajas:
            for obj in aux_objs:
                if caja == obj:
                    cantidad_co += 1            

        return cantidad_co == len(aux_cajas)
        # cantidad_co = len(aux_cajas)
        # contador_cajas_en_objetivos = 0
        # for caja in aux_cajas:
        #     for objetivo in aux_objs:
        #         if values[caja] == values[objetivo]:
        #             contador_cajas_en_objetivos += 1
        
        return cantidad_cajas_objetivos != cantidad_co  

    CAJAS_OBJETIVOS = CAJAS + OBJETIVOS
    constraints.append((CAJAS_OBJETIVOS, game_not_win))   
    
    #funcion que devuelve true si es adyacente
    def es_adyacente(pos,ady):        
        lista_adyacentes = calculo_adyacentes(pos)
        for x in lista_adyacentes:
            if ady == x:
                return True
        return False

    def calculo_adyacentes(pos):
        adyacentes = [
            (pos[0]+1,pos[1]), #abajo
            (pos[0]-1,pos[1]), #arriba
            (pos[0],pos[1]+1), #derecha
            (pos[0],pos[1]-1)  #izquierda
        ]
        movimientos = []
        for f,c in adyacentes:
            if f>=0 and f<filas and c>=0 and c<filas:
                movimientos.append((f,c))
        return movimientos

    def caja_mas_de_2_paredes_adyacentes(variables,values):
        #recibo 1 caja seguida de todas las paredes
        c = 0
        caja = values[0]
        for pared in values[1:]:
            if es_adyacente(caja,pared):
                c+=1
        if c > 1:
            return False
        elif c == 1 and len(calculo_adyacentes(caja)) < 4:
            return False
        else:
            return True

    # for celda1, celda2 in combinations(OBJ_PAREDES,2):
    #     constraints.append(((celda1, celda2), different))
    for caja in CAJAS:
        if len(PAREDES) > 1:
            for celda1, celda2 in combinations(PAREDES,2):
                constraints.append((([caja] + [celda1]+ [celda2]), caja_mas_de_2_paredes_adyacentes))
        else:
            constraints.append((([caja]+ PAREDES), caja_mas_de_2_paredes_adyacentes))

    # Restriccion de mas de una pared adyacente
    # def dos_paredes_adyacentes_caja(variables,values):
    #     aux_cajas = []       
    #     aux_paredes = []    
    #     #cantidad_co = 0
        
    #     for idx, vari in enumerate(variables):
    #         # expresión regular para saber si es caja               
    #         if re.search("^caja[0-9]+", vari):
    #             aux_cajas.append(values[idx])
    #         elif re.search("^pared[0-9]+", vari):
    #             aux_paredes.append(values[idx])
    #     for caja in aux_cajas:
            

    #         cont_paredes_ady = 0
    #         for mov in movimientos:
    #             if mov in aux_paredes:
    #                 cont_paredes_ady += 1
        
    #         if cont_paredes_ady >= 2:
    #             return False
    #         elif len(movimientos) < 4 and cont_paredes_ady >= 1:
    #             return False
    #         else:
    #             return True

    # CAJAS_PAREDES = CAJAS + PAREDES
    # constraints.append((CAJAS_PAREDES,dos_paredes_adyacentes_caja))   

    # Restriccion de no ubicar cajas en esquinas   
    for caja in CAJAS:       
        if (0,0) in domains[caja]:
            domains[caja].remove((0,0))
        if (0,columnas-1) in domains[caja]:
            domains[caja].remove((0,columnas-1))
        if (filas-1,0) in domains[caja]:
            domains[caja].remove((filas-1,0))
        if (filas-1,columnas-1) in domains[caja]:    
            domains[caja].remove((filas-1,columnas-1))



    
    
    problema = CspProblem(problem_variables, domains, constraints)
    resultado = backtrack(problema,variable_heuristic=LEAST_CONSTRAINING_VALUE)
    #print(resultado)
    lista_cajas = []
    lista_objetivos = []
    lista_paredes = [] 
    
    for key in resultado.keys():
        if re.search("^caja[0-9]+", key):
            lista_cajas.append(resultado[key])
        elif re.search("^pared[0-9]+", key):
            lista_paredes.append(resultado[key])
        elif re.search("^objetivo[0-9]+", key):
            lista_objetivos.append(resultado[key])        
           
    return (lista_paredes, lista_cajas, lista_objetivos,resultado['PJ'])
#caso_mediano_reducido = armar_mapa(5, 5, 4, 3)