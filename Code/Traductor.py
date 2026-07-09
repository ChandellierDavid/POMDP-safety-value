from os import listdir
from random import sample
from random import randint
from random import random

def is_number(string):
    try:
        int(string)
        return(True)
    except ValueError:
        return(False)

def traduction(f):
    states = []
    actions = []
    observations = []
    c = 2

    i = 0
    while (f[i:i+6] != "states"):
        i += 1
    i += 8
    while (f[i] != "\n"):
        state = ""
        while ((f[i] != " ") and (f[i] != "\n")):
            state += f[i]
            i += 1
        states.append(state)
        if (f[i] != "\n"):
            i += 1
    
    if (len(states) == 1):
        if is_number(states[0]):
            n = int(states[0])
        else:
            n = 1
            states_bij = {states[0] : 0}
    else:
        number = False
        n = len(states)
        states_bij = {}
        for j in range(n):
            states_bij[states[j]] = j
    
    if (n > 20):
        print("test too big, the algorithm will take to much time, this test has not been added", end = "\n\n")
        return(len(states),0,0,0,0,[[{0 : {}}]])
    
    i += 10
    while (f[i] != "\n"):
        action = ""
        while ((f[i] != " ") and (f[i] != "\n")):
            action += f[i]
            i += 1
        actions.append(action)
        if (f[i] != "\n"):
            i += 1

    if (len(actions) == 1):
        if is_number(actions[0]):
            m = int(actions[0])
        else:
            m = 1
            actions_bij = {actions[0] : 0}
    else:
        number = False
        m = len(actions)
        actions_bij = {}
        for j in range(m):
            actions_bij[actions[j]] = j

    i+= 15
    while (f[i] != "\n"):
        observation = ""
        while ((f[i] != " ") and (f[i] != "\n")):
            observation += f[i]
            i += 1
        observations.append(observation)
        if (f[i] != "\n"):
            i += 1

    if (len(observations) == 1):
        if is_number(observations[0]):
            o = int(observations[0])
        else:
            o = 1
            observations_bij = {observations[0] : 0}
    else:
        number = False
        o = len(observations)
        observations_bij = {}
        for j in range(m):
            observations_bij[observations[j]] = j

    init = n
    lose = n+1                                                  # on fait un nouvel état qui sera l'état perdant
    lose_obs = o                                                # on fait une nouvelle observation qui sera l'observation menant vers l'état perdant
    Delta = [[{} for _ in range(m)] for _ in range(n+c)]

    for a in range(m):
        Delta[lose][a][lose_obs] = {lose : 1}

    i += 1
    while ((f[i:i+6] != "start:") and (f[i:i+14] != "start include:") and (f[i:i+14]) != "start exclude:"):
        i += 1
    if (f[i:i+6] == "start:"):
        i += 7
        starts = []
        if (f[i:i+7] == "uniform"):
            for j in range(m):
                Delta[init][j] = {0 : {k : 1/n for k in range(n)}}
        else:
            while (f[i] != "\n"):
                start = ""
                while (f[i] != " " and f[i] != "\n"):
                    start += f[i]
                    i += 1
                starts.append(start)
                if (f[i] != "\n"):
                    i += 1
            if (len(starts) != 1):
                for j in range(n):
                    init_distr = {}
                    for k in range(n):
                        if (float(starts[k]) != 0):
                            init_distr[k] = float(starts[k])
                    Delta[init][j] = {0 : init_distr}
            else:
                if is_number(starts[0]):
                    for j in range(m):
                        Delta[init][j] = {0 : {int(starts[0]) : 1}}
                else:
                    for j in range(m):
                        Delta[init][j] = {0 : {states_bij[starts[0]] : 1}}
    elif (f[i:i+14] == "start include:"):
        i += 15
        starts = []
        while (f[i] != "\n"):
            start = ""
            while (f[i] != " " and f[i] != "\n"):
                start += f[i]
                i += 1
            starts.append(start)
            if (f[i] != "\n"):
                i += 1

        all_numbers = True
        for start in starts:
            if not(is_number(start)):
                all_numbers = False
        
        if all_numbers:
            for j in range(m):
                Delta[init][j] = {0 : {int(start) : 1/len(starts) for start in starts}}
        else:
            for j in range(m):
                Delta[init][j] = {0 : {states_bij[start] : 1/len(starts) for start in starts}}
    else:
        i += 15
        starts = []
        while (f[i] != "\n"):
            start = ""
            while (f[i] != " " and f[i] != "\n"):
                start += f[i]
                i += 1
            starts.append(start)
            if (f[i] != "\n"):
                i += 1
        
        for j in range(m):
            Delta[init][j] = {0 : {}}

        if all_numbers:
            for j in range(len(starts)):
                starts[j] = int(starts[j])
        else:
            for j in range(len(starts)):
                starts[j] = states_bij[starts[j]]
        for j in range(n):
            if j not in starts:
                for k in range(m):
                    Delta[init][k][0][j] = 1/(n-len(starts))
    i += 1

    while (f[i:i+2] != "T:"):
        i += 1

    transitions = [[] for _ in range(m)]
    for _ in range(m):
        i += 2
        act = ""
        while (f[i] != "\n"):
            act += f[i]
            i += 1
        i += 1
        ord = 0
        abs = 0
        transition = [[0 for _ in range(n)] for _ in range(n)]
        while (f[i:i+2] != "T:" and f[i:i+2] != "O:"):
            while(f[i] != "\n"):
                transition_proba = ""
                while (f[i] != " " and f[i] != "\n"):
                    transition_proba += f[i]
                    i += 1
                if (transition_proba == "identity"):
                    for j in range(n):
                        transition[j][j] = 1.00
                else:
                    transition[ord][abs] = float(transition_proba)
                    abs += 1
                if (f[i] != "\n"):
                    i += 1
            ord += 1
            abs = 0
            i += 1
        transitions[actions_bij[act]] = transition

    observations = [[] for _ in range(m)]
    for _ in range(m):
        i += 2
        act = ""
        while (f[i] != "\n"):
            act += f[i]
            i += 1
        i += 1
        ord = 0
        abs = 0
        observation = [[0 for _ in range(o)] for _ in range(n)]
        while (i < len(f) and f[i:i+2] != "O:"):
            while(i < len(f) and f[i] != "\n"):
                observation_proba = ""
                while (i < len(f) and f[i] != " " and f[i] != "\n"):
                    observation_proba += f[i]
                    i += 1
                observation[ord][abs] = float(observation_proba)
                abs += 1
                if (i < len(f) and f[i] != "\n"):
                    i += 1
            ord += 1
            abs = 0
            i += 1
        observations[actions_bij[act]] = observation
    
    for q1 in range(n):
        for a in range(m):
            for q2 in range(n):
                t = transitions[a][q1][q2]
                if (t != 0):
                    for obs in range(o):
                        if (observations[a][q2][obs] != 0):
                            if obs not in Delta[q1][a]:
                                Delta[q1][a][obs] = {q2 : t*observations[a][q2][obs]}
                            else:
                                Delta[q1][a][obs][q2] = t*observations[a][q2][obs]
    
    to_lose = sample(range(n),randint(0,n-1))
    for i in range(len(to_lose)):
        q1 = to_lose[i]
        lose_act = sample(range(m),randint(1,m-1))
        for j in range(len(lose_act)):
            a = lose_act[j]
            p = random()
            for obs in Delta[q1][a].keys():
                for q2 in Delta[q1][a][obs].keys():
                    Delta[q1][a][obs][q2] *= 1-p
            Delta[q1][a][lose_obs] = {lose : p}

    return((n+c,m,o+1,init,lose,Delta))

tests = []
folder = listdir("Benchmark")
k1 = 0
k2 = 0

with open("Traduced.py", "w") as trad:
    trad.write("tests = []\n\n")

    for file in folder:
        k1 += 1
        f = open("Benchmark/"+file,'r')
        f = f.read()
        print("Traducting file :", file)
        (n,m,o,init,lose,Delta) = traduction(f)
        if (n <= 20):
            k2 += 1
            trad.write("#\n#                    Test : "+str(k2)+", Traduction of "+file+"\n#\n\n")
            trad.write("n = "+str(n)+"\n")
            trad.write("m = "+str(m)+"\n")
            trad.write("o = "+str(o)+"\n")
            trad.write("init = "+str(init)+"\n")
            trad.write("lose = "+str(lose)+"\n")
            trad.write("Delta = "+str(Delta)+"\n")
            trad.write("tests.append((n,m,o,init,lose,Delta))\n\n")
            print("Traducted file\nNumber of files traducted : ",k2,"\nTotal number of files : ",k1, end = "\n\n")
print("fin de la traduction")