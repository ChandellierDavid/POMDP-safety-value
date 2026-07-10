from fractions import Fraction

data = {}                                   # data contiendra des données utilisées uniquement dans des fonctions imbriquées dans une autre qui n'utilise pas ce paramètre, je veux que des paramètres "utiles" dans mes fonctions

class POMDP:
    def __init__(self,n,k,p,init,lose,Delta):
        self.nb_state = n                   # les états sont nommés de 0 à (n-1)
        self.nb_act = k                     # les actions sont nommées de 0 à (k-1)
        self.nb_obs = p                     # les observation sont nomées de 0 à (p-1)
        self.init = init                    # état initial
        self.lose = lose                    # état perdant, pas nécessaire dans le cas général mais dans notre cas si
        self.transition = Delta             # matrice de dictionnaire de dictionnaire (premier élément un état, second une action, troisième une observation et quatrième un état) une case contient la proba d'aller en un état et d'avoir l'observation en faisant une action à partir d'un état, on suppose que lose est absorbant
        return

    def decode(self,k):                                                                     # On décode le binaire pour trouver les états dans la partie, on rajoute un flag si lose est dans t (pour la suite)
        t = []
        shift = 1
        for i in range(k.bit_length()):
            if (k & shift):
                t.append(i)
            shift <<= 1
        return(t)
    
    def sort(self,x):
        return(-len(self.decode(x)))

#
#           construction des beliefs perdants
#

    def transition_belief(self,t,a,o):                                                      # k est un entier encodant le belief le i-ème bit vaut 1 si qi est dans le belief, a une action, et o une observation
        new_belief = 0
        seen = [False for _ in range(self.nb_state)]

        for i in t:
            if o in self.transition[i][a]:
                for j in self.transition[i][a][o].keys():                                   # état atteignable depuis i en prenant l'action a et en observant o
                    if not(seen[j]):    
                        new_belief += 2**j
                        seen[j] = True
        return(new_belief)

    def belief_graph(self):                                                                 # on indexe pas les arêtes par les observations ni les actions car c'est inutile pour le calcul des états perdants
        nb_belief = 2**self.nb_state
        U = [[] for _ in range(nb_belief)]                                                  # tableau dont les cases sont des tableaux tels que sa case d'indice i est le sommet de V obtenu en faisant l'action i à la fin seul U[0] vaut -1
        V = [[] for _ in range(nb_belief*self.nb_act)]                                      # tableau dont les cases sont des tableaux tels que sa case d'indice i est le sommet de U atteint en observant l'observation i et -1 si on ne peut pas avoir l'observation

        card = 0
        for i in range(nb_belief):
            t = self.decode(i)
            for a in range(self.nb_act):
                U[i].append(card)
                seen = [False for _ in range(self.nb_obs)]
                for j in t:
                    for o in self.transition[j][a].keys():
                        if (not(seen[o])):
                            seen[o] = True
                            m = self.transition_belief(t,a,o)
                            V[card].append(m)
                card += 1
        return(U,V)
        
    def reverse_belief_graph(self,U,V):
        nb_belief = 2**(self.nb_state + 1) - 1
        Up = [[] for _ in range(nb_belief)]                                                 # mirroir de U mais on fait juste des propriétés sur l'existence où l'universalité de certain chemin dont les observations et actions ne servent plus
        Vp = [-1 for _ in range(nb_belief*self.nb_act)]                                     # mirroir de V

        for i in range(len(U)):
            for j in range(len(U[i])):
                v = U[i][j]
                Vp[v] = i                                                                   # les sommets de v sont de degré entrant 1 dont le mirroir a degré sortant 1, pas besoin de liste d'adjacence
        for i in range(len(V)):
            for j in range(len(V[i])):
                u = V[i][j]
                Up[u].append(i)                                                             # les sommets de u n'ont pas forcément degré entrant 1
        return(Up,Vp)
    
    def winning_believes(self):                                                             # on va calculer l'attracteur des beliefs avec l'état lose, on calcul le complémentaire de safety
        nb_belief = 2**self.nb_state
        (U,V) = self.belief_graph()
        (Up,Vp) = self.reverse_belief_graph(U,V)
        winning_neighbors_u = [len(U[i]) for i in range(nb_belief)]
        losing_U = [False for i in range(nb_belief)]
        losing_V = [False for i in range(nb_belief*self.nb_act)]
        new_u = []
        new_v = []

        for i in range(nb_belief):
            if ((len(bin(i)) > self.lose + 2) and int(bin(i)[-1-self.lose]) == 1):          # proba non nulle d'être sur l'état perdant, on met des believes non accessible pour diminuer le cardinal du complémentaire
                losing_U[i] = True
                new_u.append(i)

        while (new_u != [] or new_v != []):                                                 # on a rajouter des sommets perdants
            if (new_u != []):                                                               # ils sont dans U
                while (new_u != []):
                    u = new_u.pop()
                    t = Up[u]                                                               # potentiels nouveau sommets perdants de V
                    for j in t:
                        if not(losing_V[j]):
                            losing_V[j] = True                                              # J2 veut atteindre lose, donc il peut l'atteindre si il peut atteindre un sommet qui ne peut pas l'éviter
                            new_v.append(j)
            else:
                while(new_v != []):
                    v = new_v.pop()
                    i = Vp[v]
                    winning_neighbors_u[i] -= 1
                    if (winning_neighbors_u[i] == 0):                                       # J1 veut éviter lose, il ne peut pas l'éviter si tous ces voisins peuvent l'atteindre
                        losing_U[i] = True
                        new_u.append(i)
        
        losing_U[0] = True
        return(complementary(losing_U))                                                     # états perdant de J1, les seuls utiles
    
    def maximal_believes(self,t):                                                           # renvoie les believes maximaux pour l'inclusion
        if (t == []):
            return([])
        else:
            n = len(t)
            t.sort(key = self.sort)
            card_max = len(self.decode(t[0]))
            max = [t[0]]
            c = 1
            while ((c < n) and (len(self.decode(t[c])) == card_max)):
                max.append(t[c])
                c += 1
            for i in range(c,n):
                elem = t[i]
                included = False
                for maxi in max:
                    if not(elem & ~maxi):                                                   # calcule si elem est inclu dans maxi avec des opérations bit à bit
                        included = True
                if not(included):
                    max.append(elem)
            return(max)

#
#               calcul de la safety value à epsilon près
#

    def min_proba(self):
        mini = 1
        for i in range(self.nb_state):
            for a in range(self.nb_act):
                for dico in self.transition[i][a].values():
                    for p in dico.values():
                        if (p < mini):
                            mini = p
        return(mini)

    def approximation(self,belief):
        approx = []
        for i in range(self.nb_state):
            qi = belief[i]
            k = int(Fraction(qi,data["mu"]))
            if (abs(k*data["mu"] - qi) < abs((k+1)*data["mu"] - qi)):
                approx.append(k*data["mu"])
            else:
                approx.append((k+1)*data["mu"])
        return(approx)

    def encode_belief(self,belief):                                                    # le .join et map servent à avoir une complexité linéaire en n car les strong sont immutables
        s = "_"
        if data["frac"]:
            return(s.join(map(str,belief)))
        else:
            return(s.join(map(str,(map(float,belief)))))

    def almost_winning(self,winning,belief):                                        # avoiding sera les tableau des états perdants maximaux pour l'inclusion, le belief sera cette fois-ci donner par un tableau donnant une distribution de proba sur les états
        for b in winning:
            t = self.decode(b)
            s = 0
            for q in t:
                s += belief[q]
            if (s >= 1 - data["epsilon"]):
                return(True)
        return(False)
    
    def update_belief(self,parents,children,lose_proba,winning_belief,new_believes,code_belief,new_belief,a,s,n):
        code_win = "win"
        if self.almost_winning(winning_belief,new_belief):                          # un long truc pour mettre à jour les dictionnaire parents et enfants et ne pas mettre de doublon
            if (code_win,n) not in parents:
                parents[(code_win,n)] = {}
            if a not in parents[(code_win,n)]:
                parents[(code_win,n)][a] = [(code_belief,n-1)]
            else:
                if ((code_belief,n-1) not in parents[(code_win,n)][a]):
                    parents[(code_win,n)][a].append((code_belief,n-1))
            
            if (code_belief,n-1) not in children:
                children[(code_belief,n-1)] = [[] for _ in range(self.nb_act)]
            if (code_win,n,s) not in children[(code_belief,n-1)][a]:
                children[(code_belief,n-1)][a].append((code_win,n,s))
                if (code_win,n) not in lose_proba:
                    lose_proba[(code_win,n)] = (0,0,[0 for _ in range(self.nb_act)],[0 for _ in range(self.nb_act)])
        else:
            code_new_belief = self.encode_belief(new_belief)
            if (code_new_belief,n) not in parents:
                parents[(code_new_belief,n)] = {}
            if a not in parents[(code_new_belief,n)]:
                parents[(code_new_belief,n)][a] = [(code_belief,n-1)]
            else:
                if (code_belief,n-1) not in parents[(code_new_belief,n)][a]:
                    parents[(code_new_belief,n)][a].append((code_belief,n-1))
            
            if (code_belief,n-1) not in children:
                children[(code_belief,n-1)] = [[] for _ in range(self.nb_act)]
            if (code_new_belief,n,s) not in children[(code_belief,n-1)][a]:
                children[(code_belief,n-1)][a].append((code_new_belief,n,s))
                if (code_new_belief not in new_believes):
                    lose_proba[(code_new_belief,n)] = (int(new_belief[self.lose]),1,[int(new_belief[self.lose]) for _ in range(self.nb_act)],[1 for _ in range(self.nb_act)])
                    new_believes[code_new_belief] = new_belief
        return
    
    def update_proba(self,parents,children,lose_proba,code,action,n):                               # trouver un moyen de mettre à jour la proba de pnp
        proba_min = 0
        proba_max = 0

        for (k,i,s) in children[(code,n)][action]:
            (p1,p2,_,_) = lose_proba[(k,i)]
            proba_min += p1*s
            proba_max += p2*s                                                                       # proba de perdre en jouant l'action a = somme (proba de perdre sur un état accessible*proba d'y aller)

        (q1,q2,qb1,qb2) = lose_proba[(code,n)]
        qb1[action] = proba_min
        qb2[action] = proba_max
        p1 = min(qb1)
        p2 = min(qb2)

        if ((p1 > q1) or (p2 < q2)):                                                                # la proba de perdre sur code force la mise à jour des probas de ces parents
            lose_proba[(code,n)] = (p1,p2,qb1,qb2)
            for a in parents[(code,n)].keys():
                for (parent,i) in parents[(code,n)][a]:
                    self.update_proba(parents,children,lose_proba,parent,a,i)
        return

    def update(self,parents,children,lose_proba,winning_belief,actual_belief,n):
        new_believes = {}

        for code_belief in actual_belief.keys():
            belief = actual_belief[code_belief]
            for a in range(self.nb_act):
                proba_obs = [0 for _ in range(self.nb_obs)]                                         # l'indice o va contenir la probabilité d'avoir l'observation o depuis le belief belief
                for i in range(self.nb_state):
                    for o in self.transition[i][a].keys():
                        for v in self.transition[i][a][o].values():
                            proba_obs[o] += v*belief[i]
                
                for o in range(self.nb_obs):
                    if (proba_obs[o] != 0):                                                         # on a bien un belief accessible depuis l'observation o
                        new_belief = [0 for _ in range(self.nb_state)]
                        for j in range(self.nb_state):                                              # calcul de la proba d'être dans l'état i
                            if o in self.transition[j][a].keys():
                                for k in self.transition[j][a][o].keys():
                                    new_belief[k] += belief[j]*self.transition[j][a][o][k]/proba_obs[o]
                        
                        if (data["mu"] != -1):                                                              # on approxime nos beliefs
                            new_belief = self.approximation(new_belief)

                        self.update_belief(parents,children,lose_proba,winning_belief,new_believes,code_belief,new_belief,a,proba_obs[o],n)
                self.update_proba(parents,children,lose_proba,code_belief,a,n-1)
        (pmin,pmax,_,_) = lose_proba[(data["code_init"],0)]
        return(new_believes,pmin,pmax)

    def safety_value(self,epsilon,frac = True,mu = -1):                                                    # calcul de la safety value
        data["frac"] = frac
        data["epsilon"] = epsilon
        data["mu"] = mu
        init = [0 for i in range(self.nb_state)]
        init[self.init] = 1
        code_init = self.encode_belief(init)
        data["code_init"] = code_init
        parents = {(code_init,0) : {i : [(code_init,0)] for i in range(self.nb_act)}}               # parents : dictionnaire de parents indexé par les beliefs contenant un dictionnaire de parents indexé par les actions dont on obtient l'enfant via l'action (utile pour update les proba)
        children = {}                                                                               # children : dictionnaire indexé par un belief conteant des tableau d'indice sur les actions contenant : un tableau (d'enfant, proba de passer de parent à enfant en choisissant l'action)
        actual_believes = {code_init : init}
        lose_proba = {(code_init,0) : (0,1,[0 for _ in range(self.nb_act)],[1 for _ in range(self.nb_act)])} # on  rajoute deux tableau indexé par les actions pour réduire la complexité de la mise à jour des proba et bien mettre à jour les probas
        winning_belief = self.maximal_believes(self.winning_believes())                                      # on considère que gagner c'est ne pas perdre

        print("     Maximal winning believes : ", end = "")
        if (winning_belief == []):
            print("none")
        else:
            for i in range(len(winning_belief)):
                if (i < len(winning_belief) -1):
                    print(self.decode(winning_belief[i]), end = ", ")
                else:
                    print(self.decode(winning_belief[i]))

        pnp = 1
        pnm = 0
        n = 1
        while (abs(pnm-pnp) > epsilon):
            (actual_believes,pnm,pnp) = self.update(parents,children,lose_proba,winning_belief,actual_believes,n)
            n += 1
            if frac:
                if (len(bin(pnm.numerator))+len(bin(pnm.denominator)) >= 40):
                    print("         Computation of the safety value in progress, current estimation :",float(1-pnm))
                else:
                    print("         Computation of the safety value in progress, current estimation :",1-pnm)
            else:
                print("         Computation of the safety value in progress, current estimation :",1-pnm)
        return(1-pnm)

def complementary(believes):
    comp = []
    for i in range(len(believes)):
        if not(believes[i]):
            comp.append(i)
    return(comp)