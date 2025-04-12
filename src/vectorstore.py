
from typing import List
from sentence_transformers import CrossEncoder
from langchain_core.documents import Document

class Vectorstore:
  model:CrossEncoder
  
  def __init__(self,documents:List[Document]):
    self.documents:List[Document] = documents
    self.model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2',max_length=512)
    
