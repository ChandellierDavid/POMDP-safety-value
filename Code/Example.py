examples = []

#
#   Example 1
#

n = 5
init = 0
lose = 4
m = 2
o = 3
lose_obs = 2
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][0] = {3 : 1}
Delta[0][1][1] = {2 : 1}
Delta[1][0][0] = {2 : 1}
Delta[1][1][1] = {3 : 1}
Delta[2][0][0] = {2 : 1}
Delta[2][1][1] = {2 : 1}
Delta[3][0][2] = {4 : 1}
Delta[3][1][2] = {4 : 1}
Delta[4][0][2] = {4 : 1}
Delta[4][1][2] = {4 : 1}

examples.append((n,m,o,init,lose,Delta))

#
#   Example 2
#

n = 5
init = 0
lose = 4
m = 2
o = 3
lose_obs = 2
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][0] = {3 : 1}
Delta[0][1][1] = {2 : 0.5, 3 : 0.5}
Delta[1][0][0] = {2 : 0.5, 3 : 0.5}
Delta[1][1][1] = {3 : 1}
Delta[2][0][0] = {2 : 1}
Delta[2][1][1] = {2 : 1}
Delta[3][0][2] = {4 : 1}
Delta[3][1][2] = {4 : 1}
Delta[4][0][2] = {4 : 1}
Delta[4][1][2] = {4 : 1}

examples.append((n,m,o,init,lose,Delta))
#
#   Example 3
#

n = 2
init = 0
lose = 1
m = 1
o = 1
lose_obs = 0
Delta = [[{0 : {1 : 1}}],[{0 : {1 : 1}}]]

examples.append((n,m,o,init,lose,Delta))

#
#   Example 4
#
n = 13
init = 0
lose = 12
m = 2
o = 3
lose_obs = 2
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][0] = {1 : 1}
Delta[0][1][1] = {2 : 1}
Delta[12][0][2] = {12 : 1}
Delta[12][1][2] = {12 : 1}
Delta[11][0][0] = {11 : 1}
Delta[11][1][1] = {11 : 1}
Delta[10][0][0] = {11 : 1}
Delta[10][1][1] = {12 : 1}
Delta[9][0][0] = {12 : 1}
Delta[9][1][1] = {11 : 1}
for i in range(1,9):
    Delta[i][1][1] = {i+2 : 0.5, i : 0.5}
    if i%2 == 0:
        Delta[i][0][0] = {i+1 : 0.5, i : 0.5}
    else:
        Delta[i][0][0] = {i+3 : 0.5, i : 0.5}

examples.append((n,m,o,init,lose,Delta))

#
#   Example 5
#

n = 13                                                              # prend un peu de temps avant de renvoyer une valeur
init = 0
lose = 12
m = 2
o = 3
lose_obs = 2
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][0] = {1 : 1}
Delta[0][1][1] = {2 : 1}
Delta[12][0][2] = {12 : 1}
Delta[12][1][2] = {12 : 1}
Delta[11][0][0] = {12 : 1}
Delta[11][1][1] = {12 : 1}
Delta[10][0][0] = {11 : 1}
Delta[10][1][1] = {12 : 1}
Delta[9][0][0] = {12 : 1}
Delta[9][1][1] = {11 : 1}
for i in range(1,9):
    Delta[i][1][1] = {i+2 : 0.5, i : 0.5}
    if i%2 == 0:
        Delta[i][0][0] = {i+1 : 0.5, i : 0.5}
    else:
        Delta[i][0][0] = {i+3 : 0.5, i : 0.5}

examples.append((n,m,o,init,lose,Delta))

#
#   Example 6
#

n = 1
init = 0
lose = 0
m = 1
o = 1
lose_obs = 0
Delta = [[{0 : {0 : 1}}]]

examples.append((n,m,o,init,lose,Delta))

#
#   Example 7 : notre POMDP avec un ensemble de belief gagnant maximaux exponentiel pour n = 5
#

n = 13
init = 0
lose = 12
m = 2
o = 3
lose_obs = 2
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][0] = {1 : 1}
Delta[0][1][1] = {2 : 1}
Delta[12][0][2] = {12 : 1}
Delta[12][1][2] = {12 : 1}
Delta[11][0][0] = {11 : 1}
Delta[11][1][1] = {11 : 1}
Delta[10][0][0] = {11 : 1}
Delta[10][1][1] = {12 : 1}
Delta[9][0][0] = {12 : 1}
Delta[9][1][1] = {11 : 1}
for i in range(1,9):
    Delta[i][1][1] = {i+2 : 1}
    Delta[i][0][0] = {i+2 : 1}

examples.append((n,m,o,init,lose,Delta))

#
#   Example 8
#

n = 13
init = 0
lose = 12
m = 2
o = 3
lose_obs = 2
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][0] = {1 : 1}
Delta[0][1][1] = {2 : 1}
Delta[12][0][2] = {12 : 1}
Delta[12][1][2] = {12 : 1}
Delta[11][0][0] = {12 : 1}
Delta[11][1][1] = {12 : 1}
Delta[10][0][0] = {11 : 1}
Delta[10][1][1] = {12 : 1}
Delta[9][0][0] = {12 : 1}
Delta[9][1][1] = {11 : 1}
for i in range(1,9):
    Delta[i][1][1] = {i+2 : 1}
    Delta[i][0][0] = {i+2 : 1}

examples.append((n,m,o,init,lose,Delta))

#
#   Example 9 : figure 8 du papier des encadrants
#

n = 4
init = 0
lose = 3
m = 1
o = 2
lose_obs = 1
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][0] = {1 : 0.33, 2 : 0.33}
Delta[0][0][1] = {3 : 0.34}
Delta[1][0][0] = {1 : 1}
Delta[2][0][0] = {1 : 0.33, 2 : 0.33}
Delta[2][0][1] = {3 : 0.34}
Delta[3][0][1] = {3 : 1}

examples.append((n,m,o,init,lose,Delta))

#
#   Example 10
#

p = 0.375
n = 3

init = 0
lose = n-1
m = 1
o = n
lose_obs = n-1
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][1] = {1 : 1-p}
Delta[0][0][lose_obs] = {lose : p}
Delta[lose][0][lose_obs] = {lose : 1}
for i in range(1,n-1):
    Delta[i][0][i] = {i : 1-p}
    Delta[i][0][(i+1)%(n-1)] = {(i+1)%(n-1) : p}

examples.append((n,m,o,init,lose,Delta))

#
#   Example 11
#

p = 0.375
n = 3

init = 1
lose = n-1
m = 1
o = n
lose_obs = n-1
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][1] = {1 : 1-p}
Delta[0][0][lose_obs] = {lose : p}
Delta[lose][0][lose_obs] = {lose : 1}
for i in range(1,n-1):
    Delta[i][0][1] = {1 : 1-p}
    Delta[i][0][(i+1)%(n-1)] = {(i+1)%(n-1) : p}

examples.append((n,m,o,init,lose,Delta))

#
#   Example 12
#

p = 1/256
n = 2
init = 0
lose = 1
m = 1
o = 2
lose_obs = 1
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][1] = {1 : p}
Delta[0][0][0] = {0 : 1-p}
Delta[1][0][1] = {1 : 1}

examples.append((n,m,o,init,lose,Delta))

#
#   Example 13
#

p = 2/5
n = 3
init = 0
lose = n-1
m = 1
o = 3
lose_obs = 2
reset = 1
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[lose][0][lose_obs] = {lose : 1}
for i in range(n-2):
    Delta[i][0][0] = {i+1 : p}
    Delta[i][0][reset] = {0 : 1-p}
Delta[n-2][0][lose_obs] = {lose : p}
Delta[n-2][0][reset] = {0 : 1-p}

examples.append((n,m,o,init,lose,Delta))

#
#   Rejected example
#

"""p = 1/2
n = 13
init = 12
lose = 11
win = 10
m = (n-3)//2
o = 4
reset = 3
lose_obs = 2
win_obs = 1
delta = int(((n-3)//2)**(1/2))+1
Delta = [[{} for _ in range(m)] for _ in range(n)]

for i in range(m):
    Delta[lose][i][lose_obs] = {lose : 1}
    Delta[win][i][win_obs] = {win : 1}
    Delta[init][i][0] = {0 : 1/((n-3)//2)}
    for j in range(1,(n-3)//2):
        Delta[init][i][0][j] = 1/((n-3)//2)
    
for i in range(m-delta+1):
    for j in range((n-3)//2):
        if (j < i):
            Delta[j][i][lose_obs] = {lose : 1}
        if (j == i):
            Delta[j][i][0] = {j+5 : p}
            Delta[j][i][reset] = {init : 1-p}
        if (j > i):
            Delta[j][i][0] = {j : p}
            Delta[j][i][reset] = {init : 1-p}
    for j in range((n-3)//2,n-3):
        if (j-5 < i):
            Delta[j][i][0] = {j-5 : p}
            Delta[j][i][reset] = {init : 1-p}
        if (j-5 == i):
            Delta[j][i][lose_obs] = {lose : 1}
        if (j-5 > i):
            Delta[j][i][0] = {j : p}
            Delta[j][i][reset] = {init : 1-p}

for i in range(m-delta+1,m):
    for j in range((n-3)//2):
        if (j < i):
            Delta[j][i][lose_obs] = {lose : 1}
        if (j == i):
            Delta[j][i][0] = {j+5 : 1-p}
            Delta[j][i][win_obs] = {win : p}
        if (j > i):
            Delta[j][i][0] = {j : 1-p}
            Delta[j][i][win_obs] = {win : p}
    for j in range((n-3)//2,n-3):
        if (j-5 < i):
            Delta[j][i][0] = {j-5 : 1-p}
            Delta[j][i][win_obs] = {win : p}
        if (j-5 == i):
            Delta[j][i][lose_obs] = {lose : 1}
        if (j-5 > i):
            Delta[j][i][0] = {j : 1-p}
            Delta[j][i][win_obs] = {win : p}

examples.append((n,m,o,init,lose,Delta))"""

"""n = 53                                                           # rien que l'initialisation en créant le graphe des beliefs est trop longue 2^53 ça fait beaucoup
init = 0
lose = 12
m = 2
o = 3
lose_obs = 2
Delta = [[{} for _ in range(m)] for _ in range(n)]

Delta[0][0][0] = {13 : 1}
Delta[0][1][1] = {14 : 1}
Delta[12][0][2] = {12 : 1}
Delta[12][1][2] = {12 : 1}
Delta[11][0][0] = {12 : 1}
Delta[11][1][1] = {12 : 1}
Delta[10][0][0] = {11 : 1}
Delta[10][1][1] = {12 : 1}
Delta[9][0][0] = {12 : 1}
Delta[9][1][1] = {11 : 1}
for i in range(1,9):
    Delta[i][1][1] = {i+2 : 1}
    Delta[i][0][0] = {i+2 : 1}
for i in range(13,23):
    if (i%2 == 0):
        Delta[i][0][0] = {i+1 : 0.25}
        Delta[i][0][1] = {i+2 : 0.25}
        Delta[i][1][0] = {i+1 : 0.25}
        Delta[i][1][1] = {i+2 : 0.25}
    else:
        Delta[i][0][0] = {i+2 : 0.25}
        Delta[i][0][1] = {i+3 : 0.25}
        Delta[i][1][0] = {i+2 : 0.25}
        Delta[i][1][1] = {i+3 : 0.25}
c = 23
offset = 23
for i in range(5):
    for j in range(5-i-1):
        Delta[c][0][0] = {c+1 : 0.5}
        Delta[c][0][1] = {c+1 : 0.5}
        Delta[c][1][0] = {c+1 : 0.5}
        Delta[c][1][1] = {c+1 : 0.5}
        c += 1
    Delta[c][0][0] = {2*i + 1 : 1}
    Delta[c][0][1] = {2*i + 1 : 1}
    Delta[c][1][0] = {2*i + 1 : 1}
    Delta[c][1][1] = {2*i + 1 : 1}
    c += 1
    Delta[13+2*i][0][0][offset] = 0.25
    Delta[13+2*i][0][1][offset] = 0.25
    Delta[13+2*i][1][0][offset] = 0.25
    Delta[13+2*i][1][1][offset] = 0.25
    offset += 5-i

    for j in range(5-i-1):
        Delta[c][0][0] = {c+1 : 0.5}
        Delta[c][0][1] = {c+1 : 0.5}
        Delta[c][1][0] = {c+1 : 0.5}
        Delta[c][1][1] = {c+1 : 0.5}
        c += 1
    Delta[c][0][0] = {2*i + 2 : 1}
    Delta[c][0][1] = {2*i + 2 : 1}
    Delta[c][1][0] = {2*i + 2 : 1}
    Delta[c][1][1] = {2*i + 2 : 1}
    c += 1
    Delta[13+2*i+1][0][0][offset] = 0.25
    Delta[13+2*i+1][0][1][offset] = 0.25
    Delta[13+2*i+1][1][0][offset] = 0.25
    Delta[13+2*i+1][1][1][offset] = 0.25
    offset += 5-i

example.append((P.POMDP(n,init,lose,m,o,Delta)))"""