import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, world!"}],
        max_tokens=5
    )
    print("API Key is working.")
    print(response.choices[0].message['content'].strip())
except openai.error.AuthenticationError as e:
    print(f"AuthenticationError: {e}")
except openai.error.OpenAIError as e:
    print(f"OpenAIError: {e}")