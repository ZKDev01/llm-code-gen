from abc import abstractmethod
import re
from typing import List,Dict
from unittest.mock import Base
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage


model_info = {
  'gemma': 'gemma3:1b',
  'deepseek': 'deepseek-r1:1.5b'
}


class ChatHistory:
  def __init__(self,m:str='default',t:float=0.8) -> None:
    """## Chat History

    Args:
        m (str): . Defaults to 'default' for 'gemma3:1b' model.
        t (float): LLM's temperature. Defaults to 0.8.
    """
    if m in model_info.keys():
      self.llm:ChatOllama = ChatOllama(model=model_info[m],temperature=t)
    else: self.llm:ChatOllama = ChatOllama(model=model_info['gemma'],temperature=t)
  
  def _simple_query(self,query:str) -> str:
    return self.llm.invoke(query).content
  
  @abstractmethod
  def _get_python_code(response:str) -> List:
    python_code_blocks = re.findall(r'```python(.*?)```', response, re.DOTALL)
    return [code.strip() for code in python_code_blocks]
  
  def generate_code(self, problem:str) -> BaseMessage:
    division:Dict = {}
    self.problem = problem
    
    # make query
    response = self._simple_query(self.problem)
    
    # take codes from response 
    division['code'] = ChatHistory._get_python_code(response)
    
    # return query and code generation
    return response,division


