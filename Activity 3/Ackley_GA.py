#!Python3

from tkinter import *
import math
import random
import functools
import numpy as np
from typing import List
#Chromosomes bits long
L_chromosome=30  #4
N_chains=2**(L_chromosome/2) #Ya que se está usando un solo cromosoma para X y Y
#Lower and upper limits of search space
a=-40
b=40
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
N_chromosomes=10
#probability of mutation
prob_m=0.50 #0 ->.25

F0=[]
fitness_values=[]

for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    fitness_values.append(0)

#binary codification
def decode_chromosome(chromosome):
    global L_chromosome,N_chains,a,b, crossover_point
    value=0
    for p in range(crossover_point):
        value+=(2**p)*chromosome[-1-p]

    return a+(b-a)*float(value)/(N_chains-1) #in Python3, conversion to float is not needed


#Original function
#def f(x):
#    return 0.05*x*x-4*math.cos(x)

#def f(x):
#    """Rastrigin Function"""
#    d = 1 #dimension
#    return 10*d + (x**2 - 10 * math.cos( 2 * math.pi * x ))



def f(chromosome: List[float]):
    """Ackley function"""
    firstSum = 0.0
    secondSum = 0.0
    for c in chromosome:
        firstSum += c**2.0
        secondSum += math.cos(2.0*math.pi*c)
    n = float(2)
    return -20.0*math.exp(-0.2*math.sqrt(firstSum/n)) - math.exp(secondSum/n) + 20 + math.e


def diviCR(cromosoma: List[int]) -> List[int] and List[int]:
    """Divide un cromosoma en su parte X y su parte Y"""
    global crossover_point
    return cromosoma[:crossover_point], cromosoma[crossover_point:]


def obtenerAckleyCromosoma(cromosoma: List[int]) -> float:
    """Obtiene el valor decodificado y de Ackley de un cromosoma
    Tomando en cuenta que este tiene una parte X y una parte Y"""
    vx, vy = diviCR(cromosoma)
    vx=decode_chromosome(vx)
    vy=decode_chromosome(vy)
    return f([vx, vy])


def evaluate_chromosomes():
    global F0
    for p in range(N_chromosomes):
        fitness_values[p]= obtenerAckleyCromosoma(F0[p])


def compare_chromosomes(chromosome1,chromosome2):
    fvc1 = obtenerAckleyCromosoma(chromosome1)
    fvc2 = obtenerAckleyCromosoma(chromosome2)
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
    F0.sort(key=functools.cmp_to_key(compare_chromosomes)) #Ordenar cromosomas por el más valioso
    print( "Best solution so far:" )
    x, y = diviCR(F0[0])
    print( "f("+str(decode_chromosome(x))+
    ","+str(decode_chromosome(y))+") = "+
    str(obtenerAckleyCromosoma(F0[0])))

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
    for i in range(30):
        nextgeneration()
    print('Otro? s/n')
    if input() == 'n':
        exit()