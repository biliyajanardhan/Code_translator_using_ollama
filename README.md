# Code Translator

A Streamlit web app that translates source code from one programming language to another using CodeLlama and LLaMA3 models, and generates documentation and run instructions for the translated code.

---

## Features

- Upload source code or text files in various formats (`.py`, `.js`, `.java`, `.cpp`, `.c`, `.ts`, `.rb`, `.go`, `.txt`, `.pdf`, `.docx`).
- Translate the uploaded code into a selected target programming language.
- Display the original code, translated code, and generated documentation side-by-side.
- Provide step-by-step instructions on how to run the translated code.
- Download the translated code file with the appropriate file extension.
- Supports on-premise AI models through Ollama API (`CodeLlama` for translation, `LLaMA3` for documentation and run steps).

---

## Technologies Used

- [Streamlit](https://streamlit.io/) — for building the interactive web interface.
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/) — to extract text from PDF files.
- [python-docx](https://python-docx.readthedocs.io/en/latest/) — to extract text from DOCX files.
- [Requests](https://docs.python-requests.org/en/latest/) — to call the Ollama local API for AI-powered code translation and explanation.
- Ollama AI Models:
  - `codellama` — for code translation.
  - `llama3` — for documentation and running instructions generation.


