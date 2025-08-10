import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Loads listing data and builds an embedding index using FAISS
def build_vectorstore(csv):
    df = pd.read_csv(csv)

    # Combine title + description into one searchable text
    df["full_text"] = df["title"] + " " + df["description"]

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(df["full_text"].to_list(), embeddings)

    return vectorstore, df

def search(vectorstore, query, k=3):
    # Finds k most relevant listings for a query

    results = vectorstore.similarity_search(query, k=k)
    return results