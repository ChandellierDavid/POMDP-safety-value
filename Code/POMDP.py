from fractions import Fraction

class POMDP:
    def __init__(self,n,init,lose,losing_obs,k,p,Delta):
        self.init = init                    # état initial
        self.lose = lose                    # état perdant, pas nécessaire dans le cas général mais dans notre cas si
        self.losing_obs = losing_obs        # observation menant à l'état perdant, pas nécessaire non plus
        self.nb_state = n                   # les états sont nommés de 0 à (n-1)
        self.nb_act = k                     # les actions sont nommées de 0 à (k-1)
        self.nb_obs = p                     # les observation sont nomées de 0 à (p-1)
        self.transition = Delta             # matrice de dictionnaire de dictionnaire (premier élément un état, second une action, troisième une observation et quatrième un état) une case contient la proba d'aller en un état et d'avoir l'observation en faisant une action à partir d'un état, on suppose que lose est absorbant
        return(None)

    def decode(self,k):                                                                     # On décode le binaire pour trouver les états dans la partie, on rajoute un flag si lose est dans t (pour la suite)
        b = bin(k)
        t = []
        n = len(b)

        for i in range(n-2):
            c = int(b[-i-1])
            if c:
                t.append(i)
        return(t)

#
#           construction des beliefs perdants
#

    def transition_belief(self,k,a,o):                                                      # k est un entier encodant le belief le i-ème bit vaut 1 si qi est dans le belief, a une action, et o une observation
        new_belief = 0
        t = self.decode(k)
        deja_vu = [False for _ in range(self.nb_state)]

        for i in t:
            if o in self.transition[i][a]:
                for j in self.transition[i][a][o].keys():                                   # état atteignable depuis i en prenant l'action a et en observant o
                    if not(deja_vu[j]):    
                        new_belief += 2**j
                        deja_vu[j] = True
        return(new_belief)

    def belief_graph(self):                                                                 # on indexe pas les arêtes par les observations ni les actions car c'est inutile pour le calcul des états perdants
        nb_belief = 2**self.nb_state
        lose_belief = 2**self.lose                                                          # singleton état perdant
        U = [[] for _ in range(nb_belief)]                                                  # tableau dont les cases sont des tableaux tels que sa case d'indice i est le sommet de V obtenu en faisant l'action i à la fin seul U[0] vaut -1
        V = [[] for _ in range(nb_belief*self.nb_act)]                                      # tableau dont les cases sont des tableaux tels que sa case d'indice i est le sommet de U atteint en observant l'observation i et -1 si on ne peut pas avoir l'observation

        card = 0
        for i in range(nb_belief):
            t = self.decode(i)
            for a in range(self.nb_act):
                U[i].append(card)
                obs = []
                for j in t:
                    obs += (self.transition[j][a].keys())
                obs = no_repetition(obs)
                for o in obs:
                    if (obs == self.losing_obs):
                        V[card].append(lose_belief)
                    else:
                        m = self.transition_belief(i,a,o)
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
    
    def losing_belief(self):                                                                # on va calculer l'attracteur des beliefs avec l'état lose, on calcul le complémentaire de safety
        nb_belief = 2**self.nb_state
        (U,V) = self.belief_graph()
        (Up,Vp) = self.reverse_belief_graph(U,V)
        winning_neighbors_u = [len(U[i]) for i in range(nb_belief)]
        losing_U = [False for i in range(nb_belief)]
        losing_V = [False for i in range(nb_belief*self.nb_act)]
        new_u = []
        new_v = []

        for i in range(nb_belief):
            if ((len(bin(i)) > self.lose + 2) and int(bin(i)[-1-self.lose]) == 1):          # proba non nulle d'être sur l'état perdant
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
        return(losing_U)                                                                    # états perdant de J1, les seuls utiles

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

    def approximation(self,belief,mu):
        approx = []
        dist = []
        for i in range(self.nb_state):
            qi = belief[i]
            qi = Fraction(qi)
            k = int(Fraction(qi,mu))
            maxi = min(1,(k+1)*mu)                                                          # on ne veut pas dépasser la proba de 1
            if (abs(k*mu - qi) < abs(maxi - qi)):
                approx.append(k*mu)
                dist.append((abs(k*mu - qi),i))
            else:
                approx.append(maxi)
                dist.append((maxi,i))
        s = 0
        for i in range(self.nb_state):
            s += approx[i]
        if (s != 1):
            dist.sort(key = tri)
            nb = (1-s)/mu
            c = 0
            if (s < 1):
                while (nb != 0):                                                            # a un moment nb vaudra 0 car nb est plus petit que le nombre de fois où on a baisser la proba
                    (d,i) = dist[c]
                    if (approx[i] < belief[i]):
                        approx[i] += mu
                        nb -= 1
                    c += 1
            else:
                while (nb != 0):                                                            # de même pour -nb
                    (d,i) = dist[c]
                    if (approx[i] > belief[i]):
                        approx[i] -= mu
                        nb += 1
                    c += 1
        return(approx)   

    def encode_belief(self,belief):
        s = ""
        for p in belief:
            s += str(p)+"_"
        return(s)

    def almost_winning(self,epsilon,winning,belief):                                         # avoiding sera les tableau des états perdants maximaux pour l'inclusion, le belief sera cette fois-ci donner par un tableau donnant une distribution de proba sur les états
        for b in winning:
            t = self.decode(b)
            s = 0
            for q in t:
                s += belief[q]
            if (s >= 1 - epsilon):
                return(True)
        return(False)
    
    def update_belief(self,parents,children,lose_proba,new_believes,new_belief,epsilon,a,s,winning_belief,code_win,code_belief,n):
        if self.almost_winning(epsilon,winning_belief,new_belief):                          # un long truc pour mettre à jour les dictionnaire parents et enfants et ne pas mettre de doublon
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
                lose_proba[(code_win,n)] = (0,0,[0 for _ in range(self.nb_act)],[0 for _ in range(self.nb_act)])
        else:
            code_new_belief = self.encode_belief(new_belief)
            if (code_new_belief,n) not in parents:
                parents[(code_new_belief,n)] = {}
            if a not in parents[(code_new_belief,n)]:
                parents[(code_new_belief,n)][a] = [(code_belief,n-1)]
            else:
                if (code_belief,s) not in parents[(code_new_belief,n)][a]:
                    parents[(code_new_belief,n)][a].append((code_belief,n-1))
            
            if (code_belief,n-1) not in children:
                children[(code_belief,n-1)] = [[] for _ in range(self.nb_act)]
            if (code_new_belief,n,s) not in children[(code_belief,n-1)][a]:
                children[(code_belief,n-1)][a].append((code_new_belief,n,s))
                lose_proba[(code_new_belief,n)] = (new_belief[self.lose],1,[new_belief[self.lose] for _ in range(self.nb_act)],[1 for _ in range(self.nb_act)])
                new_believes.append(new_belief)
        return()
    
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
        return(None)

    def update(self,parents,children,lose_proba,actual_belief,winning_belief,epsilon,code_init,n,mu):
        code_win = self.encode_belief([0 for _ in range(self.nb_state)])
        new_believes = []

        for belief in actual_belief:
            code_belief = self.encode_belief(belief)
            for a in range(self.nb_act):
                for o in range(self.nb_obs):                                                        # on fait l'action a et on a vu l'observation o
                    s = 0                                                                           # c'est la proba d'avoir l'oservation o qui servira à normaliser la proba que l'on va calculer (la somme des s sur les observation vaut 1)
                    for i in range(self.nb_state):
                        s1 = 0
                        if o in self.transition[i][a]:
                            for v in self.transition[i][a][o].values():
                                s1 += v
                        s += belief[i]*s1

                    if (s != 0):                                                                    # on a bien un belief accessible depuis l'observation s
                        new_belief = [0 for _ in range(self.nb_state)]
                        for j in range(self.nb_state):                                              # calcul de la proba d'être dans l'état i
                            if o in self.transition[j][a].keys():
                                for k in self.transition[j][a][o].keys():
                                    new_belief[k] += belief[j]*self.transition[j][a][o][k]/s
                        
                        if (mu != -1):                                                              # on approxime nos beliefs
                            new_belief = self.approximation(new_belief,mu)
                    
                        self.update_belief(parents,children,lose_proba,new_believes,new_belief,epsilon,a,s,winning_belief,code_win,code_belief,n)
                self.update_proba(parents,children,lose_proba,code_belief,a,n-1)
        (pmin,pmax,_,_) = lose_proba[(code_init,0)]
        return(new_believes,pmin,pmax)

    def safety_value(self,epsilon,mu = -1):                                                         # calcul de la safety value
        init = [0 for i in range(self.nb_state)]
        init[self.init] = 1
        code_init = self.encode_belief(init)
        parents = {(code_init,0) : {i : [(code_init,0)] for i in range(self.nb_act)}}               # parents : dictionnaire de parents indexé par les beliefs contenant un dictionnaire de parents indexé par les actions dont on obtient l'enfant via l'action (utile pour update les proba)
        children = {}                                                                               # children : dictionnaire indexé par un belief conteant des tableau d'indice sur les actions contenant : un tableau (d'enfant, proba de passer de parent à enfant en choisissant l'action)
        actual_believes = [init]
        lose_proba = {(code_init,0) : (0,1,[0 for _ in range(self.nb_act)],[1 for _ in range(self.nb_act)])} # on  rajoute deux tableau indexé par les actions pour réduire la complexité de la mise à jour des proba et bien mettre à jour les probas
        winning_belief = maximal_elements(complementary(self.losing_belief()))                      # on considère que gagner c'est ne pas perdre
        pnp = 1
        pnm = 0
        n = 1
        while (abs(pnm-pnp) > epsilon):
            (actual_believes,pnm,pnp) = self.update(parents,children,lose_proba,actual_believes,winning_belief,epsilon,code_init,n,mu)
            n += 1
            print("         Computation of the safety value in progress, current estimation :",1-pnm)
        return(1-pnm)

def inclusion(x,y):
    bx = bin(x)
    by = bin(y)
    nx = len(bx)
    ny = len(by)
    if nx > ny:                                                                                     # l'écriture en binaire de x est plus longue que celle de y donc l'indice du bit de poids fort de x n'est pas dans le belief représenté par y
        return(False)
    else:
        for i in range(2,nx):
            if ((int(bx[i]) == 1) and (int(by[i]) != 1)):                                           # un élément de x n'est pas dans y
                return(False)
        return(True)

# On pourrais faire une implémentation des éléments maximaux sous forme d'un ZDD, cela permettrait de réduire la complexité moyenne de la taille de la représentation de l'ensemble et du test d'appartenance mais pas la complexité asymptotique.

def tri(x):
    (x1,x2) = x
    return(-x1)

def maximal_elements(t):
    n = len(t)
    max = []
    for i in range(n):
        pop = []
        inclu = False
        for k in max:
            if inclusion(t[i],k):                                                                   # on regarde si il y a un élément dans lequel on est inclu si non, on est maximal
                inclu = True
            if inclusion(k,t[i]):
               pop.append(i)
        new_max = []
        i0 = 0
        for j in range(len(max)):
            if (max[j] == pop[i0]):
                i0 += 1
            else:
                new_max.append(max[j])
        max = new_max
        if not(inclu):
            max.append(t[i])
    return(max)

def complementary(believes):
    comp = []
    for i in range(len(believes)):
        if not(believes[i]):
            comp.append(i)
    return(comp)

def no_repetition(t):
    out = {}
    for o in t:
        if o not in out:
            out[o] = 1
    return(out.keys())