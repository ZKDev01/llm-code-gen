from typing import List
from src.chat_history import ChatHistory


# insert your problem here
name_outputs = 'suma_arrays'
problem = """ 
Hazme un algoritmo en Python que resuelva:
Dado un array de enteros `nums` y un objetivo `target`, encontrar una subsecuencia (no continua) de números que sumen `target` y devolver sus índices

Example: [2, 3, 3, 5, 7, 2, 3], target = 6
Output: index (1,2) : [3,3]
"""


#region Test Functions
def final_test():
  llm = ChatHistory()
  response,codes = llm.problem_solver(problem=problem)
  save_response(response=response)
  executes_codes(codes=codes)

def simple_test():
  llm = ChatHistory()
  response,codes = llm.generate_code(problem=problem)
  save_response(response=response)
  executes_codes(codes=codes)

def chat_test():
  llm = ChatHistory()
  llm._query_in_memory("Desarrolla un algoritmo de Fibonacci en Python")
  for m in llm.memory:
    print(m.content)
  input()
  
  llm._query_in_memory("Explicame el algoritmo y cual es su complejidad")
  for m in llm.memory:
    print(m.content)
#endregion


#region Save/Test Outputs
def save_response(response:str) -> None:
  with open(f"{name_outputs}.md", 'w', encoding='utf-8') as f:
    f.write(response)

def executes_codes(codes:List[str]) -> None:
  error_counter = 0
  
  for i,code in enumerate(codes):
    file_path = f"{name_outputs}_{i}.py"
    with open(file_path,'w',encoding='utf-8') as f:
      f.write(code)
    
    try:
      exec(open(file_path).read())
      print("The file executed successfully without errors")
    except Exception as e:
      print(f"An Error Ocurred while Executing the file: {e}")
      error_counter+=1
  
  print(f"Error: {error_counter} of {len(codes)} Codes")
#endregion


def main() -> None:
  #simple_test()
  #chat_test()
  final_test()

if __name__ == "__main__":
  main()

