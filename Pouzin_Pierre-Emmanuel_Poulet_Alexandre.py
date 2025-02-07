import random

class Cellule:
    def __init__(self):
        self.nord = None
        self.sud = None
        self.est = None
        self.ouest = None

    def modif(self, nord, sud, est, ouest):
        self.nord = nord
        self.sud = sud
        self.est = est
        self.ouest = ouest
        
    def __str__(self):
        liste = [self.nord, self.sud, self.est, self.ouest]
        return " ".join(map(str, liste))

class Grille:
    def __init__(self, n):
        self.lig = n
        self.col = n
        self.grille = [[Cellule() for i in range(n)] for j in range(n)]


    def remplirGrille(self):
        for l in range(self.lig):
            for c in range(self.col):
                nord = random.randint(1,5)
                sud = random.randint(1,5)
                est = random.randint(1,5)
                ouest = random.randint(1,5)
                        
                if l == 0:
                    if c == 0:
                        self.grille[l][c].modif(nord, sud, est, ouest)
                        self.grille[l][c+1].modif(self.grille[l][c+1].nord, self.grille[l][c+1].sud, self.grille[l][c+1].est, est)
                    elif c == self.col-1:
                        self.grille[l][c].modif(nord, sud, est, self.grille[l][c].ouest)
                    else:
                        self.grille[l][c].modif(nord, sud, est, self.grille[l][c].ouest)
                        self.grille[l][c+1].modif(self.grille[l][c+1].nord, self.grille[l][c+1].sud, self.grille[l][c+1].est, est)
                    self.grille[l+1][c].modif(sud, self.grille[l-1][c].sud, self.grille[l-1][c].est, self.grille[l-1][c].ouest)

                elif l == self.lig-1:
                    if c == 0:
                        self.grille[l][c].modif(nord, sud, est, ouest)
                        self.grille[l][c+1].modif(self.grille[l][c+1].nord, self.grille[l][c+1].sud, self.grille[l][c+1].est, est)    
                    elif c == self.col-1:
                        self.grille[l][c].modif(nord, sud, est, self.grille[l][c].ouest)
                    else:
                        self.grille[l][c].modif(self.grille[l][c].nord, sud, est, self.grille[l][c].ouest)
                        self.grille[l][c+1].modif(self.grille[l][c+1].nord, self.grille[l][c+1].sud, self.grille[l][c+1].est, est)
                    
                elif c == 0:
                    self.grille[l][c].modif(self.grille[l][c].nord, sud, est, ouest)
                    self.grille[l][c+1].modif(self.grille[l][c+1].nord, self.grille[l][c+1].sud, self.grille[l][c+1].est, est)
                    self.grille[l+1][c].modif(sud, self.grille[l+1][c].sud, self.grille[l+1][c].est, self.grille[l+1][c].ouest)
                
                elif c == self.col-1:
                    self.grille[l][c].modif(self.grille[l][c].nord, sud, est, self.grille[l][c].ouest)
                    self.grille[l+1][c].modif(sud, self.grille[l+1][c].sud, self.grille[l+1][c].est, self.grille[l+1][c].ouest)
                
                else:
                    self.grille[l][c].modif(self.grille[l][c].nord, sud, est, self.grille[l][c].ouest)
                    self.grille[l][c+1].modif(self.grille[l][c+1].nord, self.grille[l][c+1].sud, self.grille[l][c+1].est, est)
                    self.grille[l+1][c].modif(sud, self.grille[l+1][c].sud, self.grille[l+1][c].est, self.grille[l+1][c].ouest)
                    
    def getCellule(self, lig, col):
        return self.grille[lig][col]
    
    def cellules_voisines(self,p,i,j):
        L=[]
        if j>0:
            L.append((i,j-1))
        if i>0:
            L.append((i-1,j))
        if j<p-1:
            L.append((i,j+1))
        if i<p-1:
            L.append((i+1,j))
        return L
    
    def tab_to_graph(self):
        p= self.lig
        G={}
        for i in range(p):
            for j in range(p):
                CV=self.cellules_voisines(p,i,j)
                G[p*i+j]=[]
                for coord in CV:
                    x, y = coord
                    if(p*i+j == p*x+y+1):
                        G[p*i+j].append((p*x+y, self.getCellule(x,y).est))
                    elif(p*i+j == p*x+y+self.lig):
                        G[p*i+j].append((p*x+y, self.getCellule(x,y).sud))
                    elif(p*i+j == p*x+y-1):
                        G[p*i+j].append((p*x+y, self.getCellule(x,y).ouest))
                    elif(p*i+j == p*x+y-self.lig):
                        G[p*i+j].append((p*x+y, self.getCellule(x,y).nord))
        return G
    
    def minimum(self,dico):
        m=float('inf')
        for k in dico:
            if dico[k] < m:
                m=dico[k]
                i=k
        return i
    
    def algo_dijkstra(self,G,s=0):
       D={}
       d={k: float('inf') for k in G}
       d[s]=0
       P={}
       while len(d)>0:
           k=self.minimum(d)
           for i in range(len(G[k])):
               v, c = G[k][i]
               if v not in D:
                   if d[v]>d[k]+c:
                       d[v]=d[k]+c
                       P[v]=k
           D[k]=d[k]
           del d[k]
       return D, P
   
    def chemin_min(self):
        p=self.lig
        G3=self.tab_to_graph()
        L,P=self.algo_dijkstra(G3)
        c=p*p-1
        lst=[(c//p, c%p)]
        while c!=0:
            lst=[(P[c]//p, P[c]%p)]+lst
            c=P[c]
        cout = 0
        for i in range(len(lst)-1):
            if lst[i+1][0] - lst[i][0] == 1:
                cout += self.getCellule(lst[i][0], lst[i][1]).sud
            elif lst[i+1][1] - lst[i][1] == 1:
                cout += self.getCellule(lst[i][0], lst[i][1]).est
        return lst, cout
        
    def __str__(self):
        chemin, cout = self.chemin_min()
        s = 0
        print("Grille initiale :")
        for i in range(self.lig):
            for j in range(self.col):
                    print("□ "+str(self.getCellule(i, j).est)+" ", end="")
            print("")
            for k in range(self.col):
                print(str(self.getCellule(i, k).sud)+" - ", end="")
            print("")
        
        print("\nGrille percée :")
        for i in range(self.lig):
            for j in range(self.col):
                if (i,j) == chemin[s]:
                    print("X "+str(self.getCellule(i, j).est)+" ", end="")
                    s+=1
                else:
                    print("□ "+str(self.getCellule(i, j).est)+" ", end="")
            print("")
            for k in range(self.col):
                print(str(self.getCellule(i, k).sud)+" - ", end="")
            print("")
            
        print("\nChemin : "+str(chemin))
        
        print("\nCout : "+str(cout))
        return ""

G = Grille(int(input("Taille de la grille : ")))
G.remplirGrille()
print(G)