# -*- coding: utf-8 -*-
#!python3
"""
Created on Sat Feb 08 2020
Programa que otorga una solución al problema de la mochila
(Knapsack) y el de cambio de cambio de monedas 
por medio del algoritmo voraz (Greedy algorithm)
@author: RRC
"""

from typing import List, Tuple

def kpGreedy(l: List[Tuple[int, int]], c: int):
    """Recibe una lista de tuplas; (peso, valor),
    regresa un valor máximo posible, junto con una lista de tuplas de los
    objetos dentro de la mochila"""
    #Ordenar objetos por valor
    import operator
    l = sorted(l, key=operator.itemgetter(1), reverse=True)
    print(l)
    mochila=[]
    valor = 0
    peso = 0
    for objeto in l:
        if(peso+objeto[0]<=c):
            mochila.append(objeto)
            #Obtener el valor
            valor += objeto[1]
            peso += objeto[0]
        else:
            continue
    
    print('El valor máximo es: ', valor)
    print('Con un peso de: ', peso)
    print('Los objetos que entraron a la mochila fueron: ', mochila)

def cmpGreedy(d:List[int], t:int):
    """Resuelve el problema del cambio de monedas por medio del
    algoritmo voraz, tomando como base el cambio total (t) y 
    una lista de denominaciones de monedas(d)"""
    #Ordenar denominación
    d.sort(reverse=True)
    monedas = []
    cambio = 0
    for m in d:
        while(cambio+m<=t):
            monedas.append(m)
            cambio+=m
    
    print('Las monedas de cambio son: ', monedas)
    print('Cambio total: ', cambio)
    
    
if __name__ == '__main__':
    print('\t\tProblema de la mochila')
    #Insertar datos
    #Izq = Weight, Der = Value
    l = [(3,3), (4,4), (5,4), (9,10), (4,4)]
    c = 11
    print('Capacidad = ', c)
    print('Objetos:')
    print('\t<-Weight, Value->\n',l, '\n\n' )
    kpGreedy(l,c)
    
    print('\n\n\t\tProblema del cambio de monedas')
    #Insertar datos
    d = [5,2,1]
    t = 9
    print('Total = ', t)
    print('Denominaciones:')
    print(d, '\n\n' )
    cmpGreedy(d,t)
    
    
	