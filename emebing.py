import openai
import os
import pickle
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Load the scraped data from CSV
def load_data_from_csv(filename):
    df = pd.read_csv(filename)
    return df.to_dict(orient='records')

# Function to get embeddings
def get_embeddings(text):
    response = openai.Embedding.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Convert news data to embeddings
def generate_embeddings(news_list):
    for news in news_list:
        # Combine title and description to form the full text
        full_text = f"{news['title']} {news['summary']}"  # Ensure 'summary' is the correct column name
        # Get embeddings for the combined text
        news['embedding'] = get_embeddings(full_text)
    return news_list

# Save embeddings to a pickle file
def save_embeddings_to_pickle(news_list, filename="data/news_embeddings.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(news_list, f)

# Main execution
if __name__ == "__main__":
    try:
        # Load data from CSV
        news_list = load_data_from_csv(r"D:\actyst\articles.csv")

        # Generate embeddings
        news_list_with_embeddings = generate_embeddings(news_list)

        # Save embeddings
        save_embeddings_to_pickle(news_list_with_embeddings)
    except Exception as e:
        print(f"An error occurred: {e}")
