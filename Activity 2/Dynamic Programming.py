#!python3
"""
Write Python scripts to solve the following
problems using Dynamic Programming
-0/1 KP
-CMP
-Levenstain Distance (Se puede solo mostrar el total)
"""
import numpy as np
from typing import Tuple, List
from prettytable import PrettyTable

def kpProblem(c: int, l:List[Tuple[int,int]], mostrar = True):
    """Solve the Knapscak problem using dynamic programming"""
    #Num of objects
    aux = [(0,0)]
    l = aux + l
    n = len(l)
    matriz = np.zeros((n,c+1), dtype='i')
    t = PrettyTable()
    for i in range(1, n): #Start in 1, cuz the firts column are zeros
        for j in range(c+1):
            if(l[i][0]>j):
                matriz[i,j] = matriz[i-1,j]
            else:
                matriz[i,j] = max(matriz[i-1, j], matriz[i-1, j-l[i][0]] + l[i][1])
    #Objects in the Knapsack
    ptr = (n-1, c) #Last element
    aux = 0
    opti = matriz[n-1, c]
    ks=[] #Object insideo of knapsack
    #Condition, is the actual element is more than his i-1
    while(opti>aux):
        if (matriz[ptr]!=matriz[ptr[0]-1,ptr[1]]):
            v = l[ptr[0]][1] #Get value in the actual object
            ks += [l[ptr[0]]]
            ptr = (ptr[0]-1,ptr[1]-v) #i-1, and n steps to left
            aux += v
        else:
            ptr = (ptr[0]-1,ptr[1])
    if mostrar:
        print('\n\t\t\tKnapsack Problem')
        print('Capacity = ', c)
        print('Objects (Weight, Value)\n', l)
        print('\nThe optimal solution is ', opti)
        print('The objects inside of Knapsack are:', ks,'\n')
        print('Matrix:')
        for i in range(n):
            t.add_row([l[i]] + list(matriz[i]))
        t.field_names = ['(W,V)\C'] +[i for i in range(c+1)]
        print(t)

def mini(a: int ,b: int) -> int:
    """Return the minimum of two variables"""
    r = a
    if b<a:
        r = b
    return r

def cmProblem(t: int, d:List[int], mostrar = True):
    """Solve the Changing-Making problem using dynamic programming"""
    #Matriz
    n = len(d)
    m = np.zeros((n,t+1), dtype='i')
    for j in range(t+1):
        m[0,j] = j
    for i in range(1,n):
        for j in range(t+1):
            if(d[i]>j):
                m[i,j] = m[i-1,j]
            else:
                m[i,j] = mini(m[i-1,j],m[i, j-d[i]]+1)
    opti = m[n-1, t]
    ptr = (n-1, t) #Last element
    aux = 0
    coins=[] #Object insideo of knapsack
    #Condition, is the actual element is more than his i-1
    while(opti!=aux):
        if (m[ptr]!=m[ptr[0]-1,ptr[1]]):
            v = d[ptr[0]]
            coins += [v]
            ptr = (ptr[0], ptr[1]-v) #n steps to left
            aux = aux + 1
        else:
            ptr = (ptr[0]-1,ptr[1])

    if mostrar:
        ta = PrettyTable()
        print('\n\t\t\tChanging-Making problem')
        print('Total = ', t)
        print('Denominations\n', d)
        print('\nThe optimal solution are', opti, 'Coins')
        print('The coins are:', coins,'\n')
        print('Matrix:')
        for i in range(n):
            ta.add_row([d[i]] + list(m[i]))
        ta.field_names = ['D\T'] + [i for i in range(t+1)]
        print(ta)

def compL(a:str, b:str) -> int:
    """Compare if two chars are equal, and returns 0 if they are it"""
    if a==b:
        return 0
    else:
        return 1

def leven(w1: str, w2:str, mostrar = True):
    """Solve the Levenshtein distance, it takes 2 string to work"""
    w1 = '3'+ w1 #Add epsilon to strings
    w2 = '3'+ w2
    m = np.zeros((len(w2),len(w1)), dtype='i')

    for j in range(len(w1)):
        m[0,j] = j
    for i in range(len(w2)):
        m[i,0] = i

    for i in range(1, len(w2)):
        for j in range(1, len(w1)):
            m[i,j] = mini(m[i-1, j]+1, mini(m[i,j-1]+1, compL(w1[j], w2[i])+m[i-1,j-1]))
    #Tracking
    #ptr to the optimal solution
    ptr = (len(w2)-1, len(w1)-1)
    opti = m[ptr]
    way= []
    while(ptr[0]!=0):
        b = (ptr[0]-1, ptr[1]-1) #Left, up
        op = ['substitute']
        if(m[b] > m[ptr[0], ptr[1]-1]):
            b = ptr[0], ptr[1]-1 #Left
            op = ['Insertion']
        if(m[b] > m[ptr[0]-1, ptr[1]]):
            b = ptr[0]-1, ptr[1] #Up
            op = ['Deletion']
        ptr = b
        way += op
    way.reverse()
    print(m)
    if mostrar:
        ta = PrettyTable()
        print('\n\t\t\tLevenshtein distance')
        print('String 1:', w1[1:])
        print('String 2:', w2[1:])
        print('The optimal solution are', opti, 'changes')
        print('The changes are ', way)
        print('\nMatrix:')
        for i in range(len(w2)):
            ta.add_row([w2[i]] + list(m[i]))
        ta.field_names = ['w2\w1'] + [c for c in w1]
        print(ta)

if __name__ == '__main__':
    #Obtener datos de entrada
    #Capacity
    c = 11
    #Object list
    #(weight, value)
    l = [(3,3), (4,4), (5,4), (9,10),(4,4)]
    kpProblem(c, l)
    #Total
    t=9
    d=[1,2,5]
    cmProblem(t,d)
    #Levenshtein distance
    w1 = 'astra inclinant'
    w2 = 'non obligant'
    leven(w1,w2)
