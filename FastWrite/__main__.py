import argparse
import os
import zipfile
from FastWrite import file_processor, doc_generator
from FastWrite.print import readmegen, remove_think_tags

def summarize_project(documentations, llm_name):
    """
    Generate a 1-paragraph summary of the project based on the concatenated documentation.
    Uses the selected LLM for summarization.
    """
    summary_prompt = (
        "Given the following documentation for each file in a Python project, "
        "write a single concise paragraph summarizing what the entire project does, "
        "its main purpose, and its key features. Do not include code snippets. "
        "Documentation:\n\n"
        + "\n\n".join(documentations)
    )
    # Use the same LLM as selected for documentation
    if llm_name == "GROQ":
        return doc_generator.generate_documentation_groq("", summary_prompt)
    elif llm_name == "GEMINI":
        return doc_generator.generate_documentation_gemini("", summary_prompt)
    elif llm_name == "OPENAI":
        return doc_generator.generate_documentation_openai("", summary_prompt)
    elif llm_name == "OPENROUTER":
        return doc_generator.generate_documentation_openrouter("", summary_prompt)
    else:
        return "Project summary could not be generated."

def summarize_text(text, llm_name):
    """
    Generate a 1-paragraph summary for the given text using the selected LLM.
    """
    summary_prompt = (
        "Summarize the following documentation in a single concise paragraph. "
        "Describe the main purpose and key features. Do not include code snippets.\n\n"
        f"{text}"
    )
    if llm_name == "GROQ":
        return doc_generator.generate_documentation_groq("", summary_prompt)
    elif llm_name == "GEMINI":
        return doc_generator.generate_documentation_gemini("", summary_prompt)
    elif llm_name == "OPENAI":
        return doc_generator.generate_documentation_openai("", summary_prompt)
    elif llm_name == "OPENROUTER":
        return doc_generator.generate_documentation_openrouter("", summary_prompt)
    else:
        return "Summary could not be generated."

def generate_doc(code, prompt, args):
    if args.GROQ:
        return doc_generator.generate_documentation_groq(code, prompt, model=args.model or "llama-3.3-70b-versatile"), "GROQ"
    elif args.GEMINI:
        return doc_generator.generate_documentation_gemini(code, prompt, model=args.model or "gemini-2.0-flash"), "GEMINI"
    elif args.OPENAI:
        return doc_generator.generate_documentation_openai(code, prompt, model=args.model or "gpt-3.5-turbo"), "OPENAI"
    elif args.OPENROUTER:
        return doc_generator.generate_documentation_openrouter(code, prompt, model=args.model or "openrouter/quasar-alpha"), "OPENROUTER"
    else:
        return "No LLM selected.", "UNKNOWN"

def main():
    parser = argparse.ArgumentParser(description="Generate documentation for a Python file using FastWrite.")
    parser.add_argument("filename", nargs="?", default=None, help="Python source file to document. If omitted, all files in the current directory will be documented.")

    # LLM selection arguments
    parser.add_argument("--GROQ", action="store_true", help="Use GROQ for generating documentation.")
    parser.add_argument("--GEMINI", action="store_true", help="Use Gemini for generating documentation.")
    parser.add_argument("--OPENAI", action="store_true", help="Use OpenAI for generating documentation.")
    parser.add_argument("--OPENROUTER", action="store_true", help="Use OpenRouter for generating documentation.")
    parser.add_argument("--model", type=str, default=None, help="Optional model name to override default.")

    # Documentation style arguments
    parser.add_argument("--Simplify", action="store_true", help="Generate simplified documentation for broader understanding for less technical users.")
    parser.add_argument("--Formal", action="store_true", help="Generate formal and concise documentation only considering important points.")
    parser.add_argument("--Research", action="store_true", help="Generate extreme detailed documentation with both Novice Friendly and Technical levels.")
    parser.add_argument("--Custom-Prompt", type=str, default=None, help="Custom user-defined prompt (must be enclosed in quotes).")

    args = parser.parse_args()

    selected_llms = [args.GROQ, args.GEMINI, args.OPENAI, args.OPENROUTER]
    if sum(selected_llms) != 1:
        print("Error: Please specify exactly one LLM using --GROQ, --GEMINI, --OPENAI, or --OPENROUTER.")
        return

    # Compose the prompt
    prompt = "Generate high-quality, developer-friendly documentation for the following Python code Ensure you include Detailed function-level and file-level documentation and a high level slightly less technical documentation at the start to make it friendly. Do not print full code snippets of existing code, just explain them:"
    if args.Simplify:
        prompt += " Simplify the documentation to make it easy for everyone to understand, even if it means sacrificing some detail."
    elif args.Formal:
        prompt += " Make the documentation extremely formal and to the point. Ensure that it is concise and only includes the most important points. Avoid unnecessary details or explanations."
    elif args.Research:
        prompt += """ Create an extremely detailed documentation, with both a Novice Friendly explanation and a Technical Explanation. Go in depth into every aspect of the code including but not limited to:
        - Abstract: Brief summary of the entire project
        - Introduction: Overview of the problem and solution
        - Methodology: Approach and methods used"""
    if args.Custom_Prompt:
        prompt = args.Custom_Prompt

    # If no filename is provided, document all files in the current directory
    if args.filename is None:
        print("No filename provided. Documenting all Python files in the current directory (This may take a while, please be patient)...")
        cwd = os.getcwd()
        # Only document files that are not directories and not hidden
        files = [f for f in os.listdir(cwd) if os.path.isfile(f) and not f.startswith('.')]
        documentations = []
        file_summaries = []
        llm_used = None
        for file in files:
            print(f"Processing file: {file}")
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    code = f.read()
                # Only document text/code files (skip binaries)
                if not code.strip():
                    continue
            except Exception:
                continue  # skip unreadable files

            
            doc, llm_used = generate_doc(code, prompt, args)
            doc = remove_think_tags(doc)
            documentations.append(f"## {file}\n\n{doc}\n")

            
            summary = summarize_text(doc, llm_used)
            summary = remove_think_tags(summary)
            file_summaries.append(f"{file}: {summary}")

        # Generate project summary using only the file summaries
        project_summary_prompt = (
            "Given the following summaries of each file in a Python project, "
            "write a single concise paragraph summarizing what the entire project does, "
            "its main purpose, and its key features. Do not include code snippets.\n\n"
            + "\n".join(file_summaries)
        )
        summary = summarize_text(project_summary_prompt, llm_used)
        summary = remove_think_tags(summary)

        with open("README.md", "w", encoding="utf-8") as readme_file:
            readme_file.write(f"# Documentation generated by FastWrite using {llm_used}\n\n")
            readme_file.write(f"## Project Summary\n\n{summary}\n\n")
            for doc in documentations:
                readme_file.write(doc)
        print("Documentation for all files has been written to README.md")
        return

    # If filename is provided, proceed as before
    if not os.path.isfile(args.filename):
        if zipfile.is_zipfile(args.filename):
            code = ""
            with zipfile.ZipFile(args.filename, 'r') as myzip:
                myzip.extractall("extractedfiles")
            for filename in os.listdir('extractedfiles'):
                with open(filename, 'r') as f:
                    fcode = f.read()
                    code = code + fcode
        else:
            print(f"Error: File '{args.filename}' does not exist.")
            return
    else:
        with open(args.filename, 'r') as f:
            code = f.read()

    documentation, llm_used = generate_doc(code, prompt, args)
    documentation = remove_think_tags(documentation)
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(f"# Documentation generated by FastWrite using {llm_used}\n\n")
        readme_file.write(documentation)

    print("Documentation has been written to README.md")

if __name__ == "__main__":
    main()
