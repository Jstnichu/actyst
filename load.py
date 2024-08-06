from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('GOOGLE_API_KEY')

if openai_api_key:
    print("API key loaded successfully.")
else:
    print("Failed to load API key.")