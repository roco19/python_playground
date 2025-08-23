import os
from google import genai
from google.genai import types
from dotenv import load_dotenv, find_dotenv

#Constants
DEFAULT_MODEL = "gemini-2.5-flash-lite"
THINKING_BUDGET = 0 # Disables thinking

PROMPT_INIT_CONTEXT_EXPERT = """\
You are an expert Python developer and software architect.
You excel at writing clear, optimized, and well-structured code that follows best practices.
When there are multiple possible approaches, explain the trade-offs and then provide the best recommended solution."""

PROMPT_DECORATOR_EXPERT = """\
Add meaningful comments where appropriate.
After the code, include a short step-by-step explanation of how it works.
If performance, readability, or maintainability trade-offs exist, briefly discuss them.
If libraries, built-ins, or design patterns can improve the solution, mention them."""

PROMPT_INIT_CONTEXT_SHORT = """\
You are an expert Python developer.
You excel at writing clear, concise, and well-structured code that follows best practices.
You always give the best possible solution."""

PROMPT_DECORATOR_SHORT = """\
Add meaningful comments where appropriate.
Add a brief and clear explanation of how it works."""

PROMPT_TEMPLATE = """\
{prompt_init_context}

Query: {prompt_query}

{prompt_decorator}

Your solution:
"""

# Load environment variables from .env
load_dotenv(find_dotenv())

def build_prompt(prompt_query):
    return PROMPT_TEMPLATE.format(
        prompt_init_context=PROMPT_INIT_CONTEXT_SHORT,
        prompt_query=prompt_query,
        prompt_decorator=PROMPT_DECORATOR_SHORT)

def get_response(client, gemini_prompt, model=DEFAULT_MODEL):
    response = client.models.generate_content(
        model=model,
        contents=gemini_prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=THINKING_BUDGET)
        ),
    )
    return response.text

def print_models(client):
    models_list = client.models.list()
    print(type(models_list))
    for model in models_list:
        print(model.name)
        print(model.display_name)
        print(model.description)
        print(model.supported_actions)
        print()

def main():
    # Making a call to Gemini endpoint
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt_query = "How can I find an element in a list?"
    final_prompt = build_prompt(prompt_query)
    print(final_prompt)
    print(get_response(client, final_prompt))

if __name__ == "__main__":
    main()