import math as ma
import numpy as np
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

def main():
    M= AdjecencyMatrixSPModified(17,14)
    M.char()
    qu.QuadTree((0,0),10,10)
    return
main()


#depricated:
"""
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