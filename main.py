from typing import List
from src.chat_history import ChatHistory


problem = """ 
Dame un codigo que me permita en un matrix identificar si la matrix es simetrica o asimetrica 
"""



def main() -> None:
  llm = ChatHistory()
  response,codes = llm.generate_code(problem=problem)
  save_response(response=response)
  executes_codes(codes=codes)

def save_response(response:str) -> None:
  with open("response.md", 'w', encoding='utf-8') as f:
    f.write(response)

def executes_codes(codes:List[str]) -> None:
  error_counter = 0
  for i,code in enumerate(codes):
    file_path = f"generated_code_{i}.py"
    with open(file_path,'w',encoding='utf-8') as f:
      f.write(code)
    
    try:
      exec(open(file_path).read())
      print("The file executed successfully without errors")
    except Exception as e:
      print(f"An Error Ocurred while Executing the file: {e}")
      error_counter+=1
  
  print(f"Error: {error_counter} of {len(codes)} Codes")



if __name__ == "__main__":
  main()