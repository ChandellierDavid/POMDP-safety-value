# Structure of a POMDP

To make a POMDP with my algorithm, you need to have one initial state, one losing state, a losing observation, the number of states, observation and action and a transition function Delta.
Delta is represented as a matrix of dictionaries of dictionaries such that Delta[q1][a][o][q2] is the probability to go to q2 and observe o from q1 by doing the action a.

# What compute my algorithm

It compute the set of maximum winning believes for the inclusion (it exist a strategy that reach lose with probability 0).
It also compute an approximation of the safety value (which is the probability to lose with the best strategy starting on the initial state) for a certain epsilon.

# How to execute my algorithm

Type python3 Main.py or pypy3 Main.py in your terminal.
My algorithm will ask you to give informations such as if you want to use my examples, what representation you want :
  - the float representation compute the probabilities with float on 64 bits.
  - the exact rational one compute the probabilities as rationals (it can use more bits, a lot more but is exact) your tests need to have probabilities expressed in rational using the function Fraction from the module fractions (whereas it won't do an exact calculus).
  - the approximation one approximate each new belief that is calculated by projecting it on a grid of precision of (3*epsilon*(p^(2^n))/(log(3/epsilon)*n) for the strong one (it is the only one that have a proof on the error made by the approximation, it has not been published yet).

it will also ask for the precision value epsilon that must be given as an integer couple for the exact rational algorithm.
If you do not use our examples, your tests must be in an array containing tuples to create a POMDP then you will write the name of the array in the terminal thus the name of the file (that must be in the same folder as my algorithm).

Finally the algorithm will calculate the safety value and winning believes.

# Complexity of the algorithm

For exact rational numbers, the algorithm is in O*((a*o)^(log(1/epsilon)*(1/p)^(2^n)) where a is the number of actions, o the number of observations, n the number of states and p the smallest probability in the POMDP. (the worst case scenario is very unlikely to happen, it will be faster to compute in practice).

For approximation and float (that can be see as an approximation with mu = 2^(-52)) the algorithm is in O*((1/mu)^n) with strong approximation it becomes O*(((log(1/epsilon)^n)*(n^n))/((epsilon^n)*(p^(2^n)*(n+1))) which is only in 2 exponential (not 3 like before) but it is slower with small examples (because often a*o < n approximating as an linear cost on the number of states).

The algorithm return the safety value in a reasonable time for the majorities of POMDPs with less than 20 states (if you try you can find simple examples of POMDP with 3 states that take a lot of time to return a response).