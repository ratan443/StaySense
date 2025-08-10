"""
WHAT THIS DOES: 
- Creates a small vector database (FAISS) to store listing descriptions
- Uses OpenAI embeddings to make each description searchable by meaning
- Sets up a retriever that fetches relevant listings for a user’s query
- Passes that retrieved data into the LLM to generate a personalized recommendation
"""

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

os.environ["OPENAI_API_KEY"] = # env var

# Quick test data
listings = [
    {"id": 1, "description": "Cozy cabin near Yosemite, hot tub, hiking trails."},
    {"id": 2, "description": "Modern downtown SF loft, near nightlife and restaurants."},
    {"id": 3, "description": "Beachfront villa in Malibu with private chef service."}
]

# 1. Convert to text docs
documents = [l["description"] for l in listings]

# 2. Split text (helps with embedding large docs)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.create_documents(documents)

"""
3. Embed documents and store in FAISS vector DB
Vector DBs: Instead of traditional keyword-based searches,
    vector dbs excel at similarity searches. They use
    algorithms to find vectors (and their corresponding data)
    that are closest to a query vector. This allows for finding semantically similar items.
    Embeddings capture the semantic meaning of the data. For instance, embeddings for words
    like "happy" and "joyful" would be closer together in the vector space than "happy" and "sad"
"""
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# 4. Create a retriever and RAG chain
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"  # "stuff" means we feed all retrieved docs to the LLM at once
)

# 5. Example
query = "Find me a place near Yosemite with outdoor activities."
response = rag_chain.run(query)

print("User Query:", query)
print("AI Recommendation:", response)