import POMDP as P
import importlib as imp
from fractions import Fraction
from math import log

print("Do you want to test our examples : (Yes/No) ", end = "")
do_example = str(input())
print("\n")

if ((do_example != "Yes") and (do_example != "yes") and (do_example != "No") and (do_example != "no")):
    print("Your response to the question is not supported. Did you made a typing error ?")
    exit()

print("What representation of the probabilities you want : (f for float, q for exact rational numbers, a for aproximation of the numbers based on precision) ")
if ((do_example == "No") or (do_example == "no")):
    print("if you use the exact rational numbers you need to encode your probabilities using the module fraction and function Fraction and if you use float you need to not use it \n")
representation = str(input())
print("\n")

if ((representation == "f") or (representation == "q")):
    approx = "none"
else:
    if (representation == "a"):
        print("type of approximation value (strong,medium,weak) :")
        print("Weak will be enough for a lot of tests but strong is the only one that garantee to satisfy the precision. \n", end = "")
        approx = str(input())
        print("\n")

        if ((approx != "weak") and (approx != "Weak") and (approx != "medium") and (approx != "Medium") and (approx != "strong") and (approx != "Strong")):
            print("Your response to the question is not supported. Did you made a typing error ?")
            exit()
    else:
        print("Your response to the question is not supported. Did you made a typing error ?")
        exit()

if (representation == "q" or representation == "a"):
    print("Precision of the safety value (it has an enormous impact on the speed of the algorithm) (writen \"x y\" for x/y) : ", end = "")
    (x,y) = map(int,input().split())
    epsilon = Fraction(x,y)
else:
    print("Precision of the safety value (it has an enormous impact on the speed of the algorithm): ", end = "")
    epsilon = float(input())
print("\n")

if (do_example == "No" or do_example == "no"):

    print("Name of the array containing the tests in your file : ", end = "")
    array = str(input())
    print('\n')

    print("File you want to test (no extention) :\n your test needs to be in a python file in an array containing a tuple with respectively the number of states, actions, observations, the initial state, the losing_state, the losing_observation and the transition function \n\n", end = "")
    file = str(input())
    print("\n")
    
    module = imp.import_module(file)
    tests = getattr(module,array)
else:
    if (do_example == "Yes" or do_example == "yes"):
        if ((representation == "q") or (representation == "a")):
            import Example_fractions as ex
        else:
            import Example as ex
        tests = ex.examples

for i in range(11,12):
    (n,a,o,init,lose,lose_obs,Delta) = tests[i]
    test = P.POMDP(n,init,lose,lose_obs,a,o,Delta)
    if (approx == "none"):
        mu = -1
    else:
        p = test.min_proba()
        if ((approx == "weak") or (approx == "Weak")):
            mu = Fraction(1,int((2**((1/epsilon)**0.5))/p))
        else:
            if ((approx == "medium") or (approx == "Medium")):
                mu = Fraction(1,int((log(3/epsilon)/((epsilon/3)*(p**n))))+1)
            else:
                if ((approx == "strong") or (approx == "Strong")):
                    mu = Fraction(1,int(Fraction(Fraction(log(3/epsilon)),(Fraction(Fraction(epsilon),3)*n*(Fraction(p)**(2**n)))) + 1))                              # mu = (epsilon*(p**(2**n)))/log(1/epsilon) puis on prend la partie entière inférieure (j'ai écrit mu de cette façon pour ne l'avoir de la forme 1/k et ne pas avoir de mu = 0 ou des division par 0)
    
    winning_code = test.winning_belief()

    print("Example",i+1,":", end = "\n\n")
    print("     Winning believes : ", end = "")
    if (len(winning_code) == 1):
        print("none")
    else:
        for i in range(len(winning_code)):
            if (winning_code[i] != 0):
                if (i < len(winning_code) -1):
                    print(test.decode(winning_code[i]), end = ", ")
                else:
                    print(test.decode(winning_code[i]))
    if (mu != -1):
        pm = test.safety_value(epsilon/3)
        print("     Safety value : calculated :", pm, ", pessimistic :",max(pm-epsilon,0), ", optimistic :", min(pm+epsilon,1), end = "\n\n") # les pessimistic et optimistic sont les bornes obtenu dans le papier des encadrants
    else:
        pm = test.safety_value(epsilon/2, mu = mu)
        print("     Safety value : calculated :", pm, ", pessimistic :",max(pm-epsilon/2,0), ", optimistic :", min(pm+epsilon,1), end = "\n\n")