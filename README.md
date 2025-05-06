# FastWrite
Python Module for AI-Assisted Documentation 

## Current Statistics:
- [![PyPI Downloads](https://static.pepy.tech/badge/fastwrite)](https://pepy.tech/projects/fastwrite)
- [![PyPI](https://badge.fury.io/py/fastwrite.svg)](https://badge.fury.io/py/fastwrite)

## Overview
This module provides functionality to:
- **Process Code Files**: Extract and list Python files from a ZIP archive.
- **Generate Data Flow Diagrams**: Create a data flow chart (in Graphviz format) by analyzing Python code using the AST module.
- **Generate Documentation**: Produce detailed documentation for Python code using multiple AI models:
  - Groq-based models (remote)
  - Gemini-based models (remote)
  - OpenAI-based models (remote)
  - OpenRouter-based models (remote)
  - Ollama-based models (local)
- **Evaluate Documentation Quality**: Compute BLEU scores to compare generated documentation against a reference document.


## Installation

### Requirements
- Python 3.11
- [groq](https://pypi.org/project/groq/)
- [google-generativeai](https://pypi.org/project/google-generativeai/)
- [openai](https://pypi.org/project/openai/)
- [requests](https://pypi.org/project/requests/)
- [nltk](https://pypi.org/project/nltk/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [rouge_metric](https://pypi.org/project/rouge-metric/)

### Install Dependencies
```bash
pip install groq google-generativeai requests nltk python-dotenv openai rouge_metric
```

## Usage

### Processing Files:
```
from FastWrite import extract_zip, list_python_files, read_file
import tempfile
import os

# Specify the path to your ZIP file containing Python code
zip_file_path = "path/to/your/code.zip"

with tempfile.TemporaryDirectory() as tmp_dir:
    # Extract the ZIP file
    extract_zip(zip_file_path, tmp_dir)
    
    # List Python files in the extracted directory
    py_files = list_python_files(tmp_dir)
    
    if py_files:
        # For example, choose the first Python file as the main file
        main_file_path = os.path.join(tmp_dir, py_files[0])
        code_content = read_file(main_file_path)

```

### Generating Data Flow Diagrams:

```
from FastWrite import generate_data_flow

# Generate Graphviz code for the data flow diagram
graphviz_code = generate_data_flow(code_content)
print(graphviz_code)

```

### Generating Documentation (Express Mode):
```
# Normal Mode:
py -m FastWrite code_filename.py --LLM_NAME

# Simplified (Novice Friendly) Mode:
py -m FastWrite code_filename.py --LLM_NAME --Simplify

# Formal (Precise and to the Point) Mode:
py -m FastWrite code_filename.py --LLM_NAME --Formal

# Research (In-Depth and Elaborate Documentation):
py -m FastWrite code_filename.py --LLM_NAME --Research

# Custom (Allows you to feed a custom prompt of your own):
py -m FastWrite code_filename.py --LLM_NAME --Custom-Prompt "Enter Custom Prompt here"
```


### Generating Documentation (Groq):

```
from FastWrite import generate_documentation_groq

custom_prompt = """
Objective:
Generate high-quality, developer-friendly documentation for the following Python code Ensure you include Detailed function-level and file-level documentation and a high level slightly less technical documentation at the start to make it friendly. Do not print full code snippets of existing code, just explain them:
"""

groq_api_key = "your_groq_api_key"
groq_model = "deepseek-r1-distill-llama-70b"  # Replace with your desired model

doc_groq = generate_documentation_groq(code_content, custom_prompt, groq_api_key, groq_model)
print(doc_groq)

```

### Generating Documentation (Gemini):

```
from FastWrite import generate_documentation_gemini

custom_prompt = """
Objective:
Generate high-quality, developer-friendly documentation for the following Python code Ensure you include Detailed function-level and file-level documentation and a high level slightly less technical documentation at the start to make it friendly. Do not print full code snippets of existing code, just explain them:
"""

gemini_api_key = "your_gemini_api_key"
gemini_model = "gemini-2.0-flash"  # Replace with your desired model

doc_gemini = generate_documentation_gemini(code_content, custom_prompt, gemini_api_key, gemini_model)
print(doc_gemini)

```

### Generating Documentation (OpenAI):

```
from FastWrite import generate_documentation_openai

custom_prompt = """
Objective:
Generate high-quality, developer-friendly documentation for the following Python code Ensure you include Detailed function-level and file-level documentation and a high level slightly less technical documentation at the start to make it friendly. Do not print full code snippets of existing code, just explain them:
"""
doc_openai = generate_documentation_openai(code_content, custom_prompt)
print(doc_openai)

```

### Generating Documentation (Ollama):

```
from FastWrite import generate_documentation_ollama

custom_prompt = """
Objective:
Generate high-quality, developer-friendly documentation for the following Python code Ensure you include Detailed function-level and file-level documentation and a high level slightly less technical documentation at the start to make it friendly. Do not print full code snippets of existing code, just explain them:
"""

# Replace with your local Ollama model name (e.g., "ollama-llama-70b")
ollama_model = "ollama-llama-70b"

doc_ollama = generate_documentation_ollama(code_content, custom_prompt, ollama_model)
print(doc_ollama)

```

### Generating Documentation (OpenRouter):

```
from FastWrite import generate_documentation_openrouter

custom_prompt = """
Objective:
Generate high-quality, developer-friendly documentation for the following Python code Ensure you include Detailed function-level and file-level documentation and a high level slightly less technical documentation at the start to make it friendly. Do not print full code snippets of existing code, just explain them:
"""
doc_openrouter = generate_documentation_openrouter(code_content, custom_prompt)
print(doc_openrouter)

```

### Calculating Bleu Score:

```
from FastWrite import calculate_bleu

# Provide a reference documentation string for comparison
reference_doc = "Your reference documentation text here..."

# Basic BLEU score calculation
bleu_score = calculate_bleu(doc_llm_host, reference_doc) ##LLM host may include Groq,Gemini,OpenAI or Ollama
print("BLEU Score:", bleu_score)

# BLEU score with smoothing
# Available smoothing methods: 'method0', 'method1', 'method2', 'method3', 'method4', 'method5', 'method6', 'method7'
bleu_score_smoothed = calculate_bleu(doc_llm_host, reference_doc, smoothing_method='method1')
print("BLEU Score with Smoothing:", bleu_score_smoothed)

# Calculate BLEU score with multiple reference documents
from FastWrite import calculate_bleu_multi_reference
reference_docs = ["Reference doc 1...", "Reference doc 2..."]
bleu_score_multi = calculate_bleu_multi_reference(doc_llm_host, reference_docs, smoothing_method='method1')
print("BLEU Score with Multiple References:", bleu_score_multi)

# Calculate BLEU score directly from files
from FastWrite import calculate_bleu_from_files
bleu_score_from_files = calculate_bleu_from_files("candidate_doc.txt", "reference_doc.txt", smoothing_method='method1')
print("BLEU Score from Files:", bleu_score_from_files)

```


### Calculating Rouge Score:
```
from FastWrite.rouge import calculate_rouge

# Provide a reference documentation string for comparison
reference_doc = "Your reference documentation text here..."

# Calculate Rouge
rouge = calculate_rouge(doc_llm_host,reference_doc)
```

### Generating README File:

```
from FastWrite.print import readmegen

readmegen(doc_llm,llm_used)
```
