# LLM Code-Gen

## Description

Large language models (LLMs) have demonstrated the ability to generate code but face limitations when solving more complex problems. Existing alternatives, such as fine-tuning and external methods like RAG, have been developed to address this. This study proposes a system integrating a dynamic memory module into lightweight LLMs (e.g., Gemma-3:1b) to enhance problem-solving capabilities without modifying the LLM’s weights or relying on external methods. The architecture combines a main LLM with a secondary model, a code validator, and a memory component that stores technical and logical errors from prior interactions. During solution generation, the system detects these errors and employs an iterative feedback process to regenerate improved responses

Key Enhancements Highlighted:
- **Dynamic Memory**: Stores past errors to inform future corrections.
- **Code Validation**: Ensures generated code meets functional requirements.
- **Iterative Feedback**: Refines outputs by addressing detected issues stepwise

## Setup

1. `python -m venv env`
2. `env\Scripts\activate`
3. `pip install -r requirements.txt`