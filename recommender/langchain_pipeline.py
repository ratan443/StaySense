from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Creates a LangChain RetrievalQA pipeline where the LLM explains recommendations
def create_recommendation_chain(vectorstore):
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={
            "prompt": """
                You are a travel recommendation assistant. 
                Given some candidate listings and a user's preferences, select the best ones and explain why 
                they match the request in 3 short bullet points.
                """
        }
    )

    return chain