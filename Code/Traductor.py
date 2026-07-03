from os import listdir

def traduction(f):
    states = []
    actions = []
    observations = []

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
    i += 10
    while (f[i] != "\n"):
        action = ""
        while ((f[i] != " ") and (f[i] != "\n")):
            action += f[i]
            i += 1
        actions.append(action)
        if (f[i] != "\n"):
            i += 1
    i+= 15
    while (f[i] != "\n"):
        observation = ""
        while ((f[i] != " ") and (f[i] != "\n")):
            observation += f[i]
            i += 1
        observations.append(observation)
        if (f[i] != "\n"):
            i += 1
    i += 1
    while ((f[i:i+6] != "start:") and (f[i:i+14] != "start include:")):
        i += 1
    if (f[i:i+6] == "start:"):
        i += 7
        proba = True
    else:
        i += 15
        proba = False
    starts = []
    while (f[i] != "\n"):
        start = ""
        while (f[i] != " " and f[i] != "\n"):
            start += f[i]
            i += 1
        starts.append(start)
        if (f[i] != "\n"):
            i += 1
    i += 1

    n = len(states)
    m = len(actions)
    o = len(observations)

    states_bij = {}
    actions_bij = {}
    observations_bij = {}
    for i in range(n):
        states_bij[states[i]] = i
    for i in range(m):
        actions_bij[actions[i]] = i
    for i in range(o):
        observations_bij[observations[i]] = i

    bool = False
    lose = n                                                    # on fait un nouvel état qui sera l'état perdant
    lose_obs = len(observations)                                # on fait une nouvelle observation qui sera l'observation menant vers l'état perdant
    n += 1
    o += 1
    if (len(starts) == 1):
        init = states_bij[starts[0]]
    else:
        init = n
        n += 1
        bool = True
    
    Delta = [[{} for _ in range(m)] for _ in range(n)]
    if bool:
        init_distr = {}
        if not(proba):
            for j in range(len(starts)):
                init_distr[states_bij[starts[j]]] = 1/len(starts)
        else:
            for j in range(len(starts)):
                p = float(starts[j])
                if p != 0:
                    init_distr[j] = p
        for a in range(m):
            Delta[init][a][0] = init_distr

    while (f[i:i+2] != "T:"):
        i += 1

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
    return((n,m,o,init,lose,lose_obs,Delta))

tests = []
folder = listdir("Benchmark")
k = 0

with open("Traducted.py", "w", encoding="utf-8") as trad:
    trad.write("tests = []\n\n")

    for file in folder:
        k += 1
        trad.write("#\n#                    Traduction of "+file+"\n#\n\n")
        f = open("Benchmark/"+file,'r')
        f = f.read()
        print("fichier en cours de traduction :", file)
        (n,m,o,init,lose,lose_obs,Delta) = traduction(f)
        trad.write("n = "+str(n)+"\n")
        trad.write("m = "+str(m)+"\n")
        trad.write("o = "+str(o)+"\n")
        trad.write("init = "+str(init)+"\n")
        trad.write("lose = "+str(lose)+"\n")
        trad.write("lose_obs = "+str(lose_obs)+"\n")
        trad.write("Delta = "+str(Delta)+"\n")
        trad.write("tests.append((n,m,o,init,lose,lose_obs,Delta))\n\n")
        print("fichier traduit",k, end = "\n\n")
print("fin de la traduction")