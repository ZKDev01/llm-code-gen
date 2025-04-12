from typing import List
def sumar_lista(x,L:List[int]):
  nueva_lista = []
  for i in L:
    nueva_lista.append(i + x)
  return nueva_lista
  
L = [1,2,3]
x = 2
nL = sumar_lista(x,L)
print(nL)
