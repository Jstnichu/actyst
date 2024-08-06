import streamlit as st
import openai
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load the embeddings data
@st.cache(allow_output_mutation=True)
def load_data():
    with open("data/news_embeddings.pkl", "rb") as f:
        return pickle.load(f)

news_data = load_data()

# Function to get embeddings
def get_embeddings(text):
    response = openai.Embedding.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Find the most relevant article
def find_most_relevant(query, data):
    query_embedding = get_embeddings(query)
    embeddings = np.array([item['embedding'] for item in data])
    similarities = cosine_similarity([query_embedding], embeddings)
    index = np.argmax(similarities)
    return data[index]

# Streamlit interface
st.title("Aluminium News Chatbot")
query = st.text_input("Enter your query:")

if query:
    result = find_most_relevant(query, news_data)
    st.write(f"*Title:* {result['title']}")
    st.write(f"*Description:* {result['description']}")
    st.write(f"*Publication Date:* {result['publication_date'].strftime('%b %d, %Y %H:%M')}")