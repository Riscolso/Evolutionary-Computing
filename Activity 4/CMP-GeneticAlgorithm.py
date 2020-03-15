#!Python3
from tkinter import *
import math
import random
import functools
import numpy as np
from typing import List
L_chromosome=9  
N_chains=2**L_chromosome
#Lower and upper limits of search space
a=-20
b=20
crossover_point=int(L_chromosome/2)
T = 9



def random_chromosome():
    chromosome=[]
    for i in range(0,L_chromosome):
        if random.random()<0.1:
            chromosome.append(0)
        else:
            chromosome.append(1)

    return chromosome

#Number of chromosomes
N_chromosomes=25
#probability of mutation
prob_m=0.75 #0 ->.25

F0=[]
fitness_values=[]

for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    fitness_values.append(0)

#binary codification
def decode_chromosome(chromosome: List[int]) -> float:
    """Convierte una cadena binaria en un entero"""
    #global L_chromosome,N_chains,a,b
    chromosome = [str(num) for num in chromosome]
    chromosome = ''.join(chromosome)
    return int(chromosome, 2)


def total(c: List[int])->int:
    """Convierte un cromosoma(cadena de binarios)
    en el total de monedas"""
    #Cantidad de monedas de valor 5, de 2 y de 1
    return (5*decode_chromosome(c[:3]))+(2*decode_chromosome(c[3:6]))+decode_chromosome(c[6:9])



def f(c: List[int]) -> float:
    """Función de ajuste, determinar qué tan apto es un cromosoma"""
    global T
    #Diferencia en la cantidad de monedas y el total + cantidad de monedas
    return abs(T-total(c)) + decode_chromosome(c[:3])+decode_chromosome(c[3:6])+decode_chromosome(c[6:9])




def evaluate_chromosomes():
    global F0

    for p in range(N_chromosomes):
        #v=decode_chromosome(F0[p])
        fitness_values[p]=f(F0[p])


def compare_chromosomes(chromosome1,chromosome2):
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
    print("\t\tMejor solución" )
    print('Cambio requerido: ', T)
    print('Cambio dado: ', str(total(F0[0])))
    x5 = decode_chromosome(F0[0][:3])
    x2 = decode_chromosome(F0[0][3:6])
    x = decode_chromosome(F0[0][6:9])
    #str(f(F0[0]))
    print('Total de monedas: ',x5+x2+x)
    print('Monedas de 5: ', x5)
    print('Monedas de 2: ', x2)
    print('Monedas de 1: ', x)

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

while(True):
    nextgeneration()
    print('Otro? s/n')
    if input() == 'n':
        exit()

