# Structure of a POMDP

To make a POMDP with my algorithm, you need to have one initial state, one losing state, a losing observation, the number of states, observation and action and a transition function Delta.
Delta is represented as a matrix of dictionaries of dictionaries such that Delta[q1][a][o][q2] is the probability to go to q2 and observe o from q1 by doing the action a.

# What compute my algorithm

It compute the set of winning believes (those which it exist a strategy that reach lose with probability 0).
It also compute an approximation of the safety value (which is the probability to lose with the best strategy starting on the initial state) for a certain epsilon.

# How to execute my algorithm

Type python3 Main.py in your terminal.
My algorithm will ask you to give information such as if you want to use our example, what representation you want :
  - the float representation compute the probabilities with float on 64 bits.
  - the exact rational one compute the probabilities as rationals (it can use more bits, a lot more but is exact) your examples need to have probabilities expressed in rational using the function Fraction     from the module fractions (whereas it won't work).
  - the approximation one approximate each new belief that is calculated by projecting it on a grid of precision of 1/(2^(1/epsilon)) and preserving the fact that the belief is a probability distribution      (if not it may diverge).

it will also ask for the precision value epsilon that must be given as an integer couple for the exact rational algorithm
If you do not use our examples, your tests must be in an array containing tuples to create a POMDP then you will write the name of the array in the terminal thus the name of the file (that must be in the same folder as my algorithm).

And the algorithm will calculate the safety value and winning believes
