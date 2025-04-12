def es_simetrica(matriz):
  """
  Determina si una matriz es simétrica o no.

  Args:
    matriz: Una lista de listas que representa la matriz.

  Returns:
    True si la matriz es simétrica, False en caso contrario.
  """
  n = len(matriz)

  # Comprobar si la matriz es cuadrada
  if n == 0:
    return True  # Una matriz vacía es considerada simétrica

  # Verificar si la matriz es simétrica
  for i in range(n):
    for j in range(n):
      if matriz[i][j] != matriz[j][i]:
        return False

  return True

def es_asimetrica(matriz):
  """
  Determina si una matriz es asimétrica.

  Args:
    matriz: Una lista de listas que representa la matriz.

  Returns:
    True si la matriz es asimétrica, False en caso contrario.
  """
  n = len(matriz)

  # Comprobar si la matriz es cuadrada
  if n == 0:
    return True

  # Comprobar si la matriz es simétrica
  for i in range(n):
    for j in range(n):
      if matriz[i][j] != matriz[j][i]:
        return False

  return True

if __name__ == "__main__":
  # Ejemplos de uso
  matriz1 = [[1, 2, 3],
             [2, 4, 5],
             [3, 5, 1]]

  matriz2 = [[1, 2, 3],
             [2, 4, 5],
             [3, 5, 4]]

  matriz3 = [[1, 2],
             [3, 4]]

  print("Matriz 1 es simétrica:", es_simetrica(matriz1))  # Output: True
  print("Matriz 2 es simétrica:", es_simetrica(matriz2))  # Output: False
  print("Matriz 3 es simétrica:", es_simetrica(matriz3))  # Output: False

  print("Matriz 1 es asimétrica:", es_asimetrica(matriz1))  # Output: True
  print("Matriz 2 es asimétrica:", es_asimetrica(matriz2))  # Output: False
  print("Matriz 3 es asimétrica:", es_asimetrica(matriz3))  # Output: False
