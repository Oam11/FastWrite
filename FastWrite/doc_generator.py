import requests
import json
from groq import Groq
from google import genai  # Updated import for new google-genai
from openai import OpenAI
from .config import get_groq_api_key, get_gemini_api_key, get_openai_api_key, get_openrouter_api_key

def generate_documentation_groq(code: str, custom_prompt: str, groq_api_key: str = None, model: str = "deepseek-r1-distill-llama-70b") -> str:
    """
    Generates documentation using a Groq-based AI model.
    If no API key is provided, it will prompt for one and save it to .env.

    :param code: The Python source code.
    :param custom_prompt: A prompt string outlining documentation requirements.
    :param groq_api_key: API key for the Groq service (optional).
    :param model: The identifier of the Groq model to use.
    :return: Generated documentation as a markdown string.
    """
    if groq_api_key is None:
        groq_api_key = get_groq_api_key()
    groq_client = Groq(api_key=groq_api_key)
    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": f"{custom_prompt}\n\n{code}"}],
        model=model
    )
    doc_content = response.choices[0].message.content
    return doc_content

def generate_documentation_gemini(code: str, custom_prompt: str, gemini_api_key: str = None, model: str = "gemini-2.0-flash") -> str:
    """
    Generates documentation using a Gemini-based AI model (google-genai).
    If no API key is provided, it will prompt for one and save it to .env.

    :param code: The Python source code.
    :param custom_prompt: A prompt string outlining documentation requirements.
    :param gemini_api_key: API key for the Gemini service (optional).
    :param model: The identifier of the Gemini model to use.
    :return: Generated documentation as a markdown string.
    """
    if gemini_api_key is None:
        gemini_api_key = get_gemini_api_key()
    client = genai.Client(api_key=gemini_api_key)
    response = client.models.generate_content(
        model=model,
        contents=f"{custom_prompt}\n\n{code}",
    )
    return response.text

def generate_documentation_openai(code: str, custom_prompt: str, openai_api_key: str = None, model: str = "gpt-3.5-turbo-instruct", max_tokens: int = 1024, temperature: float = 0.7) -> str:
    """
    Generates documentation using the OpenAI API.
    If no API key is provided, it will prompt for one and save it to .env.

    :param code: The Python source code.
    :param custom_prompt: A prompt string outlining documentation requirements.
    :param openai_api_key: API key for OpenAI (optional).
    :param model: The identifier of the OpenAI model to use.
    :param max_tokens: Maximum number of tokens to generate.
    :param temperature: Sampling temperature.
    :return: Generated documentation as a markdown string.
    """
    if openai_api_key is None:
        openai_api_key = get_openai_api_key()

    client = OpenAI(api_key=openai_api_key)

    response = client.completions.create(
        model=model,
        prompt=f"{custom_prompt}\n\n{code}",
        max_tokens=max_tokens,
        temperature=temperature,
    )
    doc_content = response.choices[0].text.strip()
    return doc_content

def generate_documentation_ollama(code: str, custom_prompt: str, model: str = "ollama-llama-70b") -> str:
    """
    Generates documentation using a local Ollama model.
    Ensure your local Ollama server is running and accessible at the given URL.

    :param code: The Python source code.
    :param custom_prompt: A prompt string outlining documentation requirements.
    :param model: The identifier of the local Ollama model to use.
    :return: Generated documentation as a markdown string.
    """
    payload = {
        "model": model,
        "prompt": f"{custom_prompt}\n\n{code}"
    }
    # Adjust the URL if your Ollama endpoint is different
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    response.raise_for_status()
    result = response.json()
    return result.get("response", "")


def generate_documentation_openrouter(code: str, custom_prompt: str, openrouter_api_key: str = None, model: str = "openrouter/quasar-alpha", max_tokens: int = 1024, temperature: float = 0.7) -> str:
    """
    Generates documentation using the OpenRouter API.
    If no API key is provided, it will prompt for one and save it to .env.

    :param code: The Python source code.
    :param custom_prompt: A prompt string outlining documentation requirements.
    :param openrouter_api_key: API key for OpenRouter (optional).
    :param model: The identifier of the OpenRouter model to use.
    :param max_tokens: Maximum number of tokens to generate.
    :param temperature: Sampling temperature.
    :return: Generated documentation as a markdown string.
    """
    if openrouter_api_key is None:
        openrouter_api_key = get_openrouter_api_key()

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "HTTP-Referer": "<YOUR_SITE_URL>",  
        "X-Title": "<YOUR_SITE_NAME>",  
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"{custom_prompt}\n\n{code}"
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    doc_content = response.json()
    return doc_content
