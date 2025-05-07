import re
import random
from abc import abstractmethod
from typing import List,Dict
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

model_info = {
  'gemma': 'gemma3:1b',
  'deepseek': 'deepseek-r1:1.5b'
}


PROMPT_CODE_GEN = """
...
"""


class ChatHistory:
  def __init__(self,m:str='default',t:float=0.8) -> None:
    if m in model_info.keys():
      self.llm:ChatOllama = ChatOllama(model=model_info[m],temperature=t)
    else: self.llm:ChatOllama = ChatOllama(model=model_info['gemma'],temperature=t)
    
    self.memory:List = []
    prompt = ChatPromptTemplate.from_messages(
      [
        ('system', f'{PROMPT_CODE_GEN}'),
        MessagesPlaceholder(variable_name='memory'),
        ('human','{input}')
      ]
    )
    self.chain = prompt | self.llm
  
  def _simple_query(self,query:str,mod_query:bool=False) -> str:
    if mod_query:
      query = f"Generame un codigo en python, capaz de responder el siguiente problema: {query}"
    return self.llm.invoke(query).content
  
  def _query_in_memory(self,query:str) -> str:
    #query = ChatHistory._get_better_prompt(query)
    response = self.chain.invoke({
      'input': query,
      'memory': self.memory
    }).content
    self.memory.append( HumanMessage(content=query) )
    self.memory.append( AIMessage(content=response) )
    return response
  
  @abstractmethod
  def _get_better_prompt(problem:str) -> str:
    llm = ChatOllama(model=model_info['gemma'],temperature=0.6)
    prompt = f""" 
    Eres un asistente con la capacidad de mejorar las preguntas del usuario para convertirlo en un mejor prompt
    El prompt que generes debe: 
    1. Mantener la pregunta del usuario
    2. Mostrar algunos ejemplos de respuestas del usuario (few-shot prompt) en caso de que la pregunta del usuario no tenga o que no puedas ser capaz de generar ejemplos a partir de la pregunta
    3. Debe estar el prompt diseñado, en español, manteniendo algunas palabras exclusivas del dominio que se encuentra en la pregunta del usuario
    
    La pregunta del usuario es: {problem}
    """
    problem = llm.invoke(prompt).content
    return problem
  
  @abstractmethod
  def _get_python_code(response:str) -> List:
    python_code_blocks = re.findall(r'```python(.*?)```', response, re.DOTALL)
    return [code.strip() for code in python_code_blocks]
  
  
  def problem_solver (self,problem:str, k:int = 2):
    response,codes = self.generate_code(problem=problem)
    while k != 0:
      k=k-1
      d_errors,fix1 = ChatHistory.search_runtime_error(codes)
      if fix1:
        # feedback a traves de runtime errors 
        self.fix_runtime_error(d_errors)
      
      l_errors = ChatHistory.search_logic_error(problem,response)
      fix2 = not len(l_errors)
      if fix2:
        # feedback a traves de otros LLM con la respuesta que genere self.llm
        self.fix_logic_error(l_errors)
      
      if (not fix1) and (not fix2):
        break
      
      if self.is_terminal():
        break
      else:
        response,codes = self.generate_code(problem=problem)
    return self.generate_code(problem=problem)
  
  def generate_code(self, problem:str):
    response = self._query_in_memory(problem) # make query
    codes = ChatHistory._get_python_code(response) # take codes from response 
    return response,codes # return query and code generation

  @abstractmethod
  def search_runtime_error(codes:List[str]) -> Dict[str,str]:
    d_errors:Dict[str,str] = { }
    is_fix = False
    for i,code in enumerate(codes):
      try:
        exec(code)
        d_errors[code] = ""
      except Exception as e:
        d_errors[code] = str(e)
        is_fix = True
    return d_errors, is_fix
  
  def fix_runtime_error(self, d_errors:Dict[str,str]) -> None:
    for code,name_error in d_errors.items():
      if not len(name_error):
        query = f"He encontrado un error en tiempo de ejecución: {name_error} en {code}. ¿Cómo puedo solucionarlo?"
        self._query_in_memory(query)
  
  @abstractmethod
  def search_logic_error(problem:str,response:str) -> List[str]:
    prompt = f"Dado el problema ({problem}) y una respuesta generada por un LLM ({response}). Construyeme una lista de errores de logica que tenga la respuesta. En caso de que no veas errores, devuelve NONE"
    
    """ 
    random_value1 = round(random.uniform(0, 1),1)
    llm1 = ChatOllama(model=model_info['deepseek'], temperature=random_value1)
    """
    
    random_value2 = round(random.uniform(0, 1),1)
    llm2 = ChatOllama(model=model_info['gemma'], temperature=random_value2)
    
    
    answer = llm2.invoke(prompt).content
    if not ("NONE" in answer):
      return answer
    return []
  
  def fix_logic_error(self, l_errors:List[str]) -> None:
    for logic_error in l_errors:
      query = f"Analiza el siguiente analisis generado por un LLM de errores sobre el problema que puedes haber cometido ({logic_error})"
      self._query_in_memory(query)
  
  def is_terminal(self, verbose=True) -> bool:
    prompt = "Con el feedback obtenido y almacenado en memoria. ¿Eres capaz de resolver el problema?. Responde únicamente con `True` o `False`"
    answer = self._query_in_memory(prompt)
    if verbose:
      print(f"Entro en is_terminal y su respuesta fue: {answer}")
    try:
      value = bool(answer)
      return value
    except:
      value = 'True' in answer
      c_value = 'False' in answer
      if value and not c_value:
        return self.is_terminal()
      return value