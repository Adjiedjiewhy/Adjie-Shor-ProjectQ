import math
from random import randint
import sys
from fractions import Fraction
try:
    from math import gcd
except ImportError:
    from fractions import gcd
from builtins import input
import projectq.libs.math
from projectq.cengines import MainEngine
from projectq.backends import Simulator
from projectq.libs.math import (MultiplyByConstantModN)
from projectq.meta import Control
from projectq.ops import (All, BasicMathGate, H, Measure, X, R)
import time
import json

def run_shor(eng, q, x, showMeasure, N):
    n = int(math.ceil(math.log(q-1, 2)))
    if showMeasure:
        print("\n\tn: ", n)

    a = eng.allocate_qureg(n)
    All(H) | a

    measurements = [0] * (n)

    ctrl_qubit = eng.allocate_qubit()

    for k in range(n):
        print("K: ", k)
        current_x = pow(x, 1 << (n - 1 - k))
        print("PROBLEM1")
        H | ctrl_qubit
        with Control(eng, ctrl_qubit):
            MultiplyByConstantModN(current_x, N) | a #PROBLEM
            print("PROBLEM2")
            
        # and measure
        Measure | ctrl_qubit
        eng.flush()
        measurements[k] = int(ctrl_qubit)
        
        if showMeasure:
            print("\033[95m{}\033[0m".format(measurements[k]), end="")
            sys.stdout.flush()

    All(Measure) | a
    m = 0
    print("\n")
    for i in range(n):
            m += measurements[n - 1 - i]*1. / (1 << (i + 1)) #Value of m/q in Hayward's

    r = Fraction(m).limit_denominator(N-1).denominator #PROBLEM
    print("PROBLEM3")

    return r

#EVEN NUMBER CHECKER
def is_even_number(N):
    if N%2 == 0:
        return True
    else:
        return False
    
#PRIME NUMBER CHECKER
def is_prime_number(N):
    if N >= 2:
        for x in range(2,int(math.sqrt(N))+1):
            if not ( N % x ):
                return False
    else:
        return False
    return True

#FINDING Q
def find_q(N):
    notFound = True
    power = 1
    while(notFound):
        q = 2**power
        if(q >= N**2):
            notFound = False
        power = power + 1
    return q

def main(user_input):
    # make the compiler and run the circuit on the simulator backend
    engine = MainEngine(Simulator())
    showMeasure = True
    f1 = 0
    f2 = 0

    # print welcome message and ask the user for the number to factor
    print("\n\tShor's Algorithm")
    N = user_input
    print("\n\tFactoring N = {}: \033[0m".format(N), end="")

    #STEP1
    #Checks if N is an even number
    isEven = is_even_number(N)
    if showMeasure:
        if isEven == True:
            print("\n\tEVEN!")
        else: 
            print("\n\tODD!")
    
    #checks if N is a prime number
    isPrime = is_prime_number(N)
    if showMeasure:
        if isPrime == True:
            print("\tPRIME!")
        else: print("\tNOT PRIME!")
    #STEP1
    
    #STEP2
    #Chooses a random integer q that satisfies N^2 <= q < 2N^2
    q = find_q(N)
    if showMeasure:
        print("\tQ: ", q)
    #STEP2
    
    #STEP3
    x = 8
    #STEP3
    
    if not gcd(x, N) == 1 or isPrime or isEven:
        print("\n\tThe generated/inputted number did not satisfy the calculation requirements")
        return 2, 2
    else:
        #STEP4-10
        r = run_shor(engine, q, x, showMeasure, N)
        
        if r % 2 != 0:
            r *= 2
        #STEP4-10
        
        #STEP11
        f1 = gcd((x**int(r/2)) + 1, N)
        f2 = gcd((x**int(r/2)) - 1, N)
        print("\tFactors:", f1, " x ", f2)
        #STEP11
        
        if ((not f1 * f2 == N) and f1 * f2 > 1 and int(1. * N / (f1 * f2)) * (f1 * f2) == N):
            f1 = f1 * f2
            f2 = int(N/(f1))
            
        if f1 * f2 == N and f1 > 1 and f2 > 1:
            print("\n\tFactors found. F1: ", f1, "and F2: ", f2)
        else:
            print("\n\tFailed to calculate factors")
        return f1, f2