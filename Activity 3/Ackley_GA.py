#!Python3

from tkinter import *
import math
import random
import functools
import numpy as np
from typing import List, Tuple
#Chromosomes are 4 bits long
L_chromosome=10  #4
N_chains=2**L_chromosome
#Lower and upper limits of search space
a=-20
b=20
crossover_point=int(L_chromosome/2)




def random_chromosome():
    chromosome=[]
    for i in range(0,L_chromosome):
        if random.random()<0.1:
            chromosome.append(0)
        else:
            chromosome.append(1)

    return chromosome

#Number of chromosomes
N_chromosomes=20
#probability of mutation
prob_m=0.75 #0 ->.25

F0=[]
F = [] #Línea para dar 2D
fitness_values=[]
#fitness_values1=[] 

for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    F.append(random_chromosome())
    fitness_values.append(0)


#binary codification
def decode_chromosome(chromosome: List[int]) -> float:
    global L_chromosome,N_chains,a,b
    value=0
    for p in range(L_chromosome):
        value+=(2**p)*chromosome[-1-p]

    return a+(b-a)*float(value)/(N_chains-1) #in Python3, conversion to float is not needed


#Original function
#def f(x):
#    return 0.05*x*x-4*math.cos(x)

#def f(x):
#    """Rastrigin Function"""
#    d = 1 #dimension
#    return 10*d + (x**2 - 10 * math.cos( 2 * math.pi * x ))



def f(chromosome):
    firstSum = 0.0
    secondSum = 0.0
    for c in chromosome:
        firstSum += c**2.0
        secondSum += math.cos(2.0*math.pi*c)
    n = float(len(chromosome))
    return -20.0*math.exp(-0.2*math.sqrt(firstSum/n)) - math.exp(secondSum/n) + 20 + math.e



def evaluate_chromosomes():
    global F0, F

    for p in range(N_chromosomes):
        v=decode_chromosome(F0[p])
        v1=decode_chromosome(F[p]) #Decodificar la segunda línea
        fitness_values[p]=f([v,v1]) #Obtener el valor de ajuste de ambas decodificaciones.


def compare_chromosomes(chromosome1,chromosome2):
    vc1=decode_chromosome(chromosome1)
    vc2=decode_chromosome(chromosome2)
    fvc1=f(vc1)
    fvc2=f(vc2)
    if fvc1 > fvc2:
        return 1
    elif fvc1 == fvc2:
        return 0
    else: #fvg1<fvg2
        return -1


suma=float(N_chromosomes*(N_chromosomes+1))/2.

Lwheel=N_chromosomes*10

def create_wheel():
    global F0,fitness_values, F

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
F3=F[:] #Para la otra lista de cromosomas


def compare_chromosomesList(lcromo: Tuple[List[int]], lcromo2: Tuple[List[int]]):
    """Compara pares de cromosomas en listas"""
    #Decodificar el par de cromosomas 1 
    vc01=decode_chromosome(lcromo[0])
    vc02=decode_chromosome(lcromo[1])
    #Decodificar el par de cromosomas 2
    vc11=decode_chromosome(lcromo2[0])
    vc12=decode_chromosome(lcromo2[1])

    #Evaluarlos
    fvc1=f([vc01, vc02])
    fvc2=f([vc11, vc12])

    #Compararlos
    if fvc1 > fvc2:
        return 1
    elif fvc1 == fvc2:
        return 0
    else: #fvg1<fvg2
        return -1

def ordenarValioso() -> List[int] and List[int]:
    """Ordena pares de cromosomas por los más valiosos"""
    global F0, F, L_chromosome, N_chromosomes
    Faux = []
    #Crear una megalista donde estén las tuplas de los cromosomas que se va evaluar
    for i in range(0,N_chromosomes):
        aux = ()
        aux = (F0[i], F[i])
        Faux.append(aux)
    #Ordenarlos por el más valioso
    Faux.sort(key=functools.cmp_to_key(compare_chromosomesList))
    #Regresar la tupla de cromosomas más valiosos
    #return Faux[0][0] and Faux[0][1]
    return Faux

    


def nextgeneration():
    #F0.sort(key=functools.cmp_to_key(compare_chromosomes)) #Ordenar cromosomas por el más valioso
    Faux = ordenarValioso()
    print( "Best solution so far:" )
    print( "f("+str(decode_chromosome(Faux[0][0])) +','+
    str(decode_chromosome(Faux[0][1]))+")= "+
    str(f([decode_chromosome(Faux[0][0]), decode_chromosome(Faux[0][1])])) )

    #elitism, the two best chromosomes go directly to the next generation
    F1 = Faux[0][0]
    F3 = Faux[0][1]
    #F1[0]=F0[0]
    #F1[1]=F0[1]
    for i in range(0,int((N_chromosomes-2)/2)):
        roulette=create_wheel()
        #Two parents are selected
        p01=random.choice(roulette)
        p02=random.choice(roulette)
        p11=random.choice(roulette)
        p12=random.choice(roulette)

        #Two descendants are generated
        o01=F0[p01][0:crossover_point]
        o01.extend(F0[p02][crossover_point:L_chromosome])
        o02=F0[p02][0:crossover_point]
        o02.extend(F0[p01][crossover_point:L_chromosome])

        o11=F[p11][0:crossover_point]
        o11.extend(F[p12][crossover_point:L_chromosome])
        o12=F[p12][0:crossover_point]
        o12.extend(F[p11][crossover_point:L_chromosome])

        
        #Each descendant is mutated with probability prob_m
        if random.random() < prob_m:
            o01[int(round(random.random()*(L_chromosome-1)))]^=1
            o11[int(round(random.random()*(L_chromosome-1)))]^=1
        if random.random() < prob_m:
            o02[int(round(random.random()*(L_chromosome-1)))]^=1
            o12[int(round(random.random()*(L_chromosome-1)))]^=1
        #The descendants are added to F1
        F1[2+2*i]=o01
        F1[3+2*i]=o02

        F3[2+2*i]=o11
        F3[3+2*i]=o12

    #The new generation replaces the old one
    F0[:] = F1[:]
    F[:] = F3[:]  

#F0.sort(key=functools.cmp_to_key(compare_chromosomes))
evaluate_chromosomes()

while(True):
    nextgeneration()
    print('Otro? s/n')
    if input() == 'n':
        exit()
