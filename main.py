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
                
#avoids computing modular inverse since the edge will be given from b <-> a
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
    PRG.remEdge(0,1)
    PRG.remEdge(0,mod-1)
    PRG.remVertex(0)
    PRG.addEdge(1,mod-1)
    return PRG

def main(): 
    PRG = MakePRG(17,3)
    #print(PRG)
    print(PRG.spanningTree(4))
    print(PRG.diameter())
    return
main()
