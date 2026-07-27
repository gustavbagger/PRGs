import numpy as np
from numpy import typing as npt

def random_vector(dimension: int) -> npt.NDArray[np.float64]:
    rng = np.random.default_rng()
    return rng.random(dimension)

def power_method(
    A: npt.NDArray[np.float64],
    num_iterations: int,
) -> npt.NDArray[np.float64]:
    if A.shape[0] != A.shape[1]:
        raise ValueError("A must be a square matrix.")
    
    # Choose a random initial vector to reduce the chance
    # that it is orthogonal to the dominant eigenvector.
    b_k = random_vector(A.shape[1])

    # Normalize the initial vector.
    b_k /= np.linalg.norm(b_k)

    for _ in range(num_iterations):
        # Multiply by the matrix.
        b_k1 = A @ b_k

        # Compute the length of the new vector.
        b_k1_norm = np.linalg.norm(b_k1)

        # Stop if the new vector is within machine precision of 0.
        if np.isclose(b_k1_norm, 0.0):
            raise ValueError("Power method produced the zero vector.")

        # Normalize the vector for the next iteration.
        b_k = b_k1 / b_k1_norm
    ray = np.dot(b_k,A @ b_k)/np.linalg.norm(b_k)

    # Return the approximate dominant eigenvector.
    return abs(ray)


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
    def remEdge(self,node1:int, node2:int):
        if self.inGraph(node1) and self.inGraph(node2):
            if node2 in self.data[node1]:
                self.data[node1].remove(node2)
            if node1 in self.data[node2]:
                self.data[node2].remove(node1)
    def addVertex(self,node:int):
        self.data[node] = []
        self.vertexCount += 1
    def remVertex(self,node:int):
        if node in self.data:
            self.data.pop(node)
            self.vertexCount-=1
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
    def adjecencyMatrix0(self) -> np.array:
        array = []
        try:
            for node in self.data.keys():
                row = np.zeros(self.vertexCount)
                for index in self.data[node]:
                    row[index] += 1
                array.append(row)
            return np.array(array)
        except IndexError:
            print("Probably tried using non-PRG0 graph")
    def adjecencyMatrix(self) -> np.array:
        array = []
        try:
            for node in self.data.keys():
                row = np.zeros(self.vertexCount)
                for index in self.data[node]:
                    row[index-1] += 1
                array.append(row)
            return np.array(array)
        except IndexError:
            print("Probably tried using non-PRG graph")
    #Assumes regularity of graph
    def regularityDegree(self) -> int:
        for node in self.data.keys():
            return len(self.data[node])
    def laplacian(self) -> np.array:
        return self.regularityDegree() * np.identity(self.vertexCount) - self.adjecencyMatrix()

#    def spectralRadius(self,iterations: int = 10) -> np.float64:
#        return power_method(self.laplacian(),iterations)

        

                
#adds vertex at 0
def MakePRG0(mod: int, root: int) -> Graph:
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
    #removes the extra vertex at 0 and associated edges before connecting 1 and mod-1.
    PRG.remEdge(0,1)
    PRG.remEdge(0,mod-1)
    PRG.remVertex(0)
    PRG.addEdge(1,mod-1)
    return PRG

def main(): 
    PRG = MakePRG(17,3)
    #print(PRG)
    print(PRG.spanningTree(4))
    print(PRG.laplacian())
    print(PRG.regularityDegree())
    return
main()
