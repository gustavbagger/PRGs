from math import *
from sympy import mod_inverse

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

def main():
    print(AdjecencyMatrixNaive(13,2))
    return
main()