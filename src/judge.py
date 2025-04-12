
import os
from openai import OpenAI
from dotenv import load_dotenv

def make_a_question(question:str):

  load_dotenv() 
  model = os.getenv("model")
  api_key = os.getenv("api_key")
  base_url = os.getenv("base_url")

  client = OpenAI(
    base_url=base_url,
    api_key=api_key,
  )

  completion = client.chat.completions.create(
    extra_body={},
    model=model,
    messages=[
      {
        "role": "user",
        "content": f"{question}"
      }
    ]
  )
  return completion.choices[0].message.content


class LLM_as_judge:
  ... 