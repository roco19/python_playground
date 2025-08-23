import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Constants
SAMPLE_TEXT = f"""
You should express what you want a model to do by \
providing instructions that are as clear and \
specific as you can possibly make them. \
This will guide the model towards the desired output, \
and reduce the chances of receiving irrelevant \
or incorrect responses. Don't confuse writing a \
clear prompt with writing a short prompt. \
In many cases, longer prompts provide more clarity \
and context for the model, which can lead to \
more detailed and relevant outputs.
"""

# Load environment variables from .env
load_dotenv(find_dotenv())

def get_response(client, prompt, model="gpt-5-nano"):
    response = client.responses.create(
        model=model,
        input=prompt
    )
    return response.output_text

def main():
    # Create a client with the API key
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize the text delimited by triple backticks into a single sentence. ```{SAMPLE_TEXT}```"
    response = get_response(client, prompt)
    print(response)

if __name__ == "__main__":
    main()