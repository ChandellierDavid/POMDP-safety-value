import importlib as imp
import fractions as frac

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
    import POMDP as P
else:
    if (representation == "a"):
        import POMDP_approximation as P
    else:
        print("Your response to the question is not supported. Did you made a typing error ?")
        exit()

if (representation == "q"):
    print("Precision of the safety value (it has an enormous impact on the speed of the algorithm) (writen \"x y\" for x/y) : ", end = "")
    (x,y) = map(int,input().split())
    epsilon = frac.Fraction(x,y)
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
        if representation == "q":
            import Example_fractions as ex
        else:
            import Example as ex
        tests = ex.examples

for i in range(len(tests)):
    (n,a,o,init,lose,lose_obs,Delta) = tests[i]
    if (representation == "a"):
        mu = frac.Fraction(1,2**(int(1/epsilon)))
        test = P.POMDP(n,init,lose,lose_obs,a,o,Delta,mu)
    else:
        test = P.POMDP(n,init,lose,lose_obs,a,o,Delta)
    winning_code = P.complementary(test.losing_belief())

    print("Example",i+1,":", end = "\n\n")
    print("     Winning believes : ", end = "")
    if (len(winning_code) == 1):
        print("none")
    else:
        for i in range(len(winning_code)):
            if (winning_code[i] != 0):
                if i < len(winning_code) -1:
                    print(test.decode(winning_code[i]), end = ", ")
                else:
                    print(test.decode(winning_code[i]))
    pm = test.safety_value(epsilon/2)
    print("     Safety value : calculated :", pm, ", pessimistic :",max(pm-epsilon/2,0), ", optimistic :", min(pm+epsilon,1), end = "\n\n") # les pessimistic et optimistic sont les bornes obtenu dans le papier des encadrants