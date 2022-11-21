import itertools
import math
from random import choice

import numpy
import calculator
from object_oriented import Backpack, ContentFilter

def sphere_volume(radius):
    return math.pi*4/3*radius**3

def isolate(arg0, arg1, arg2, arg3, arg4):
    print(arg0, arg1, arg2, sep='     ', end=' ')
    print(arg3, arg4, sep=' ', end='\n')

def first_half(string):
    return string[:(int) (len(string)/2)]

def backward(string):
    return string[::-1]

def list_ops():
    animals = ["bear", "ant","cat","dog"]
    animals.append("eagle")
    animals[2] = "fox"
    animals.pop(1) #b f d e
    animals.sort()
    animals[animals.index("eagle")] = "hawk"
    animals[-1] += "hunter"
    return animals

def pig_latin(word):
    firstLetter = word[0]
    if firstLetter in ['a', 'e', 'i','o','u']:
        word += "hay"
    else:
        word = word[1:] + firstLetter + "ay"
    return word

def palindrome():
    for a in range(999,0,-1):
        for b in range(999,0,-1):
            product = a * b
            if product - (int) (backward(str(product))) == 0:
                return (a,b)

def alt_harmonic(n):
    series = []
    for i in range(1,n+1):
        series.append(((-1)**(i+1))/i)
    return sum(series)

def minMaxAverage(numbers):
    return (min(numbers), max(numbers), sum(numbers)/len(numbers))

def hypotenuse(kat1, kat2):
    return math.sqrt(calculator.sum(kat1**2, kat2**2))

def powerSet(list):
    return set(itertools.product(list,list,repeat=1))

def test_backpack():
    testpack = Backpack("Barry", "black")       # Instantiate the object.
    if testpack.name != "Barry":                # Test an attribute.
        print("Backpack.name assigned incorrectly")
    for item in ["pencil", "pen", "paper", "computer"]:
        testpack.put(item)                      # Test a method.
    print("Contents:", testpack.contents)

def random_walk(max_iters=1e12):
    try:
        walk = 0
        directions = [1, -1]
        for i in range(int(max_iters)):
            walk += choice(directions)
        print("Process completed")
        return walk
    except KeyboardInterrupt:
        print("Process interrupted at iteration " + i)

def matrixMulti():
    a = [[3,-1,4],[1,5,-9]]
    b = [[2,6,-5,3],[5,-8,9,7],[9,-3,-2,-3]]
    return numpy.dot(a,b)

def matrixOp():
    a = [[3,1,4],[1,5,9],[-5,3,1]]
    a2 = numpy.matmul(a,a)
    return -numpy.matmul(a2,a)+9*a2-15*numpy.array(a)

def largeMatrix():
    a = []
    for i in range(7):
        row = []
        for j in range (7):
            if i <= j: 
                row.append(1)
            else:  
                row.append(0)
        a.append(row)
    b = []
    for i in range(7):
        row = []
        for j in range (7):
            if i < j: 
                row.append(5)
            else:  
                row.append(-1)
        b.append(row)
    product = numpy.matmul(a,numpy.matmul(b,a))
    return numpy.array(product,numpy.int64)

def nonNegative(list):
    A = numpy.array(list)
    B = A > 0
    B.astype(numpy.int8)
    return numpy.multiply(B,A)

def weirdMatrix():
    A = numpy.array([[0,2,4],[1,3,5]])
    B = numpy.array([[3,0,0],[3,3,0],[3,3,3]])
    C = numpy.array([[-2,0,0],[0,-2,0],[0,0,-2]])
    return numpy.array([[0,numpy.transpose(A),numpy.identity(3)],[A,0,0],[B,0,C]])

def rowStochastic(matrix):
    A = numpy.array(matrix)
    B = []
    for row in A:
        B.append([1/sum(row)])
    return A*B


if __name__ == "__main__":
    print(sphere_volume(34))
    isolate(1,2,3,4,5)
    print(backward("test1"))
    print(list_ops())
    print(pig_latin("atest"))
    print(palindrome())
    print(alt_harmonic(5))
    print(minMaxAverage([12,5,3,1,35,3,1,23,5,3]))
    print(hypotenuse(1,1))
    test_backpack()
    #ContentFilter("fractidon.java")
    print(matrixOp())
    print(largeMatrix())
    print(rowStochastic([[1,3,2],[4,5,6],[7,8,9]]))
        