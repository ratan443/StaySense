from recommender.similarity_search import build_vectorstore
from recommender.langchain_pipeline import create_recommendation_chain

if __name__ == "__main__":
    vectorstore, df = build_vectorstore("data/sample_listings.csv")
    chain = create_recommendation_chain(vectorstore)
    