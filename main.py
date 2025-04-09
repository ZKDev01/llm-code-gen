import streamlit as st 
from src.model import make_a_question


def main() -> None:
  st.title("LLM- Code Gen")
  question = st.text_area(label="Insert your question")
  
  if st.button("search an answer"):
    st.write(f"The question is: {question}")
    st.write(f"The answer is: {make_a_question(question)}")

if __name__ == "__main__":
  main()
