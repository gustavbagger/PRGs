import math as ma
import numpy as np

class Tree(object):

    def __init__(self, data: list[set] | None = None):
        if data == None:
            data = []
        self.data = data

    def __str__(self) -> str:
        out = ""
        for levelSet in self.data:
            out += f"{levelSet}\n"
        return out.rstrip("\n")
    def diameter(self) -> int:
        return len(self.data)-1

    
class Graph(object):

    def __init__(self, data: dict[int:list] | None = None):
        if data == None:
            data = {}
        self.data = data
        self.vertexCount = len(data)

    def __str__(self) -> str:
        out = ""
        for vertex,edges in self.data.items():
            out += f"{vertex}: {edges}\n"
        return out.rstrip("\n")

    def addEdge(self,node1:int, node2:int):
        if self.inGraph(node1) and self.inGraph(node2):
            self.data[node1].append(node2)
            self.data[node2].append(node1)
        
    def addVertex(self,node:int):
        self.data[node] = []
        self.vertexCount += 1

    def inGraph(self,node:int) -> bool:
        return node in self.data

    def spanningTree(self, root:int) -> Tree:
        seenSet = {root}
        seen = 1
        lastLevel = {root}
        tree = [lastLevel]
        while seen < self.vertexCount:
            thisLevel = set()
            for vertex in lastLevel:
                for neighbour in self.data[vertex]:
                    if neighbour not in seenSet:
                        thisLevel.add(neighbour)
                        seenSet.add(neighbour)
                        seen+=1
            tree.append(thisLevel)
            lastLevel = thisLevel
        return Tree(tree)

    def diameter(self) -> dict:
        best = 1
        bestNode = -1
        for node in self.data.keys():
            new = self.spanningTree(node).diameter() 
            if new > best:
                best = new
                bestNode = node
        return {"diameter":best,"Root":bestNode}
                




#avoids computing modular inverse since the edge will be given from b <-> a
def MakePRG(mod: int, root: int) -> Graph:
    PRG = Graph()
    #add vertecies
    for vertex in range(mod):
        PRG.addVertex(vertex)
    #insert edges to existing verticies
    for vertex in range(mod):
        Tv = (vertex+1) % mod
        Dv = (vertex*root) % mod
        PRG.addEdge(vertex,Tv)
        PRG.addEdge(vertex,Dv)
    return PRG


def main(): 
    PRG = MakePRG(17,14)
    #print(PRG)
    print(PRG.spanningTree(4))
    print(PRG.diameter())
    return
main()


#depricated:
"""
import quads as qu

from sympy import mod_inverse, Matrix, zeros


def helperArrayAdderSP(row: int, columns: list, matrix: Matrix) -> None:
    matrix[row,columns[0]-1]+=1
    matrix[row,columns[1]-1]+=1
    matrix[row,columns[2]-1]+=1
    matrix[row,columns[3]-1]+=1
    return

def AdjecencyMatrixSP(mod: int, prim: int) -> Matrix:
    out = zeros(mod-1)
    primInv = mod_inverse(prim,mod)
    helperArrayAdderSP(0,[mod-1,2,primInv,prim],out)
    for i in range(2,mod-1):
        helperArrayAdderSP(i-1,[i-1,i+1,(i*primInv) % mod,(i*prim) % mod],out)
    helperArrayAdderSP(mod-2,[mod-2,1,mod-primInv,mod-prim],out)
    return out

def helperArrayAdderSPModified(row: int, columns: list, matrix: Matrix) -> None:
    matrix[row,columns[0]]+=1
    matrix[row,columns[1]]+=1
    matrix[row,columns[2]]+=1
    matrix[row,columns[3]]+=1
    return

def AdjecencyMatrixSPModified(mod: int, prim: int) -> Matrix:
    out = zeros(mod)
    primInv = mod_inverse(prim, mod)
    for i in range(0,mod):
        helperArrayAdderSPModified(i,[(i-1) % mod,(i+1) % mod,(i*primInv) % mod,(i*prim) % mod],out)
    return out

def PrintChar(self: Matrix) -> None:
    print(self.charpoly('x').as_expr())
    return

Matrix.char = PrintChar 


def AdjecencyMatrixNaive(mod: int, prim: int) -> list:
    out = list()
    primInv = mod_inverse(prim,mod)
    Adjecency = sorted([mod-1,2,primInv,prim])
    out.append(Adjecency)
    for i in range(2,mod-1):
        Adjecency = sorted([i-1,i+1,(i*primInv) % mod,(i*prim) % mod])
        out.append(Adjecency)
    Adjecency = sorted([mod-2,1,mod-primInv,mod-prim])
    out.append(Adjecency)
    return out

def helperArrayAdderNP(row: int, columns: list, array: np.ndarray) -> None:
    array[row,columns[0]-1]+=1
    array[row,columns[1]-1]+=1
    array[row,columns[2]-1]+=1
    array[row,columns[3]-1]+=1
    return

def AdjecencyMatrixNP(mod: int, prim: int) -> np.ndarray:
    out = np.zeros((mod-1,mod-1))
    primInv = mod_inverse(prim,mod)
    helperArrayAdderNP(0,[mod-1,2,primInv,prim],out)
    for i in range(2,mod-1):
        helperArrayAdderNP(i-1,[i-1,i+1,(i*primInv) % mod,(i*prim) % mod],out)
    helperArrayAdderNP(mod-2,[mod-2,1,mod-primInv,mod-prim],out)
    return out
"""