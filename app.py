import streamlit as st
import openai
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
from scrape_news import scrape_dynamic_news  # Import the scrape_dynamic_news function
import logging

# Load the embeddings data and update daily
@st.cache_data(ttl=86400)  # Cache for 86400 seconds (1 day)
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
st.write(f"Data last updated: {datetime.now().strftime('%b %d, %Y %H:%M')}")
query = st.text_input("Enter your query:")

# Display the result for the user's query
if query:
    filtered_news_data = [item for item in news_data if 'embedding' in item]
    if filtered_news_data:
        result = find_most_relevant(query, filtered_news_data)
        st.write(f"### {result.get('title', 'No title available')}")
        st.write(f"*{result.get('summary', 'No description available')}*")
        st.write(f"Publication Date: {result.get('date', 'No date available')}")
        st.write(f"[Link]({result.get('link', 'No link available')})")
        st.write("---")
    else:
        st.write("No news data available for the query.")

# Display top 5 news
st.subheader("Top 5 News")
top_news_data = scrape_dynamic_news()
if top_news_data:
    for i, article in enumerate(top_news_data[:5]):
        st.write(f"### {article.get('title', 'No title available')}")
        st.write(f"*{article.get('summary', 'No description available')}*")
        st.write(f"Publication Date: {article.get('date', 'No date available')}")
        st.write(f"[Link]({article.get('link', 'No link available')})")
        st.write("---")
else:
    st.write("No news available.")
