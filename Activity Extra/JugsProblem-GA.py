#!Python3
"""Script de un Algoritmo genético que resuelve el problema de los garrafones de agua
Cada gen del cromosoma es un operación
El resultado final se expresa en el primer garrafón
TODO: Agregar simbología
"""

import math
import random
import functools
import numpy as np
from typing import List, Tuple
from random import randrange

L_chromosome=8 
N_chains=2**L_chromosome
#Lower and upper limits of search space
crossover_point=int(L_chromosome/2)
#Cantidad de agua que se busca tener en un garrafón
T = 4
#Capacidad de cada garrafón
G1 = 5
G2 = 3

def hacerAccion(instruccion: int, garrafones: Tuple[int, int], mostrarPasos:bool = False) -> Tuple[int, int]:
    """Recibe un número el cual es un tipo de instrucción a realizar sobre un valor(Tupla)"""
    global G1, G2
    cadaux = ''
    #if mostrarPasos:
    #        print('Entra: ', garrafones)
    if(instruccion == 0): #Llenar el primer garrafón
        garrafones = (G1, garrafones[1])
        cadaux = '-LLenar G1 ' + str(garrafones)
    elif(instruccion == 1): #LLenar el garrafón 2
        garrafones = (garrafones[0], G2)
        cadaux = '-Llenar G2 ' + str(garrafones)
    elif(instruccion == 2): #Vaciar el garrafón 2
        garrafones = (garrafones[0], 0)
        cadaux = '-Vaciar G2 ' + str(garrafones)
    elif(instruccion == 3): #Vaciar el garrafón 1
        garrafones = (0, garrafones[1])
        cadaux = '-Vaciar G1 ' + str(garrafones)
    elif(instruccion == 4): #Pasar contenido de G2 a G1
        aux = garrafones[0] + garrafones[1]
        if aux>G1:
            garrafones = (G1, aux - G1)
        else:
            garrafones = (aux, 0)
        cadaux = '-G2 -> G1 ' + str(garrafones)
    elif(instruccion == 5): #Pasar contenido de G1 a G2
        aux = garrafones[0] + garrafones[1]
        if aux>G2:
            garrafones = (aux - G2, G2)
        else:
            garrafones = (0, aux)
        cadaux = '-G1 -> G2 '+ str(garrafones)
    if mostrarPasos:
        print(cadaux)
    return garrafones

def random_chromosome():
    """Genera los cromosomas de forma aleatoria"""
    chromosome=[]
    for i in range(0,L_chromosome):
        chromosome.append(randrange(6))
    return chromosome

#Number of chromosomes
N_chromosomes=20
#probability of mutation
prob_m=0.75 #0 ->.25

F0=[]
fitness_values=[]

#Generación de los cromosomas
for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    fitness_values.append(0)

#binary codification
def decodificarCromosoma(chromosome: List[int]) -> float:
    """A partir de un cromosoma, genera todas las instrucciones que tiene
    y regresa el valor final de primer garrafón"""
    #global L_chromosome,N_chains,a,b
    g = (0,0)
    for i in chromosome:
        g = hacerAccion(i, g)
    return g[0]

def f(c: List[int]) -> int:
    """Función de ajuste, determinar qué tan apto es un cromosoma"""
    global T
    return abs(decodificarCromosoma(c) - T)


def evaluate_chromosomes():
    global F0

    for p in range(N_chromosomes):
        #v=decode_chromosome(F0[p])
        fitness_values[p]=f(F0[p])


def compare_chromosomes(chromosome1: List[int],chromosome2: List[int]) -> int:
    #vc1=decode_chromosome(chromosome1)
    #vc2=decode_chromosome(chromosome2)
    fvc1=f(chromosome1)
    fvc2=f(chromosome2)
    if fvc1 > fvc2:
        return 1
    elif fvc1 == fvc2:
        return 0
    else: #fvg1<fvg2
        return -1


suma=float(N_chromosomes*(N_chromosomes+1))/2.

Lwheel=N_chromosomes*10

def create_wheel():
    global F0,fitness_values

    maxv=max(fitness_values)
    acc=0
    for p in range(N_chromosomes):
        acc+=maxv-fitness_values[p]
    fraction=[]
    for p in range(N_chromosomes):
        fraction.append( float(maxv-fitness_values[p])/acc)
        if fraction[-1]<=1.0/Lwheel:
            fraction[-1]=1.0/Lwheel
    fraction[0]-=(sum(fraction)-1.0)/2
    fraction[1]-=(sum(fraction)-1.0)/2

    wheel=[]

    pc=0

    for f in fraction:
        Np=int(f*Lwheel)
        for i in range(Np):
            wheel.append(pc)
        pc+=1

    return wheel

F1=F0[:]



def nextgeneration():
    F0.sort(key=functools.cmp_to_key(compare_chromosomes)) 
    global T
    #print('Cromosoma ', F0[0])
    print('Mejor solución hasta ahora: ')
    print('Cromosoma: ', F0[0])
    g = (0,0)
    for i in F0[0]:
        g = hacerAccion(i, g, True)
    print('Valor Final de cromosoma:', f(F0[0]))
    print('Cantidad Final de agua en el garrafón 1:', decodificarCromosoma(F0[0]))

    #elitism, the two best chromosomes go directly to the next generation
    F1[0]=F0[0]
    F1[1]=F0[1]
    for i in range(0,int((N_chromosomes-2)/2)):
        roulette=create_wheel()
        #Two parents are selected
        p1=random.choice(roulette)
        p2=random.choice(roulette)
        #Two descendants are generated
        o1=F0[p1][0:crossover_point]
        o1.extend(F0[p2][crossover_point:L_chromosome])
        o2=F0[p2][0:crossover_point]
        o2.extend(F0[p1][crossover_point:L_chromosome])
        #Each descendant is mutated with probability prob_m
        if random.random() < prob_m:
            o1[int(round(random.random()*(L_chromosome-1)))]^=1
        if random.random() < prob_m:
            o2[int(round(random.random()*(L_chromosome-1)))]^=1
        #The descendants are added to F1
        F1[2+2*i]=o1
        F1[3+2*i]=o2


    #The new generation replaces the old one
    F0[:]=F1[:]

F0.sort(key=functools.cmp_to_key(compare_chromosomes))
evaluate_chromosomes()
print("\t\tProblema de los garrafones por GA" )
print('Cantidad de litros que se quieren en el garrafón 1: ', T, '\n')

while(True):
    nextgeneration()
    print('Otro? s/n')
    if input() == 'n':
        exit()

