from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.services.rag.retriever import retrieve_relevant_docs

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_answer(question: str):
    relevant_docs = retrieve_relevant_docs(question)
    context = "\n".join(relevant_docs)
    
    prompt = f"""
    You are a helpful assistant for a restaurant. 
    Answer the customer's question based ONLY on the following context.
    If the context doesn't contain the answer, say you don't know and suggest they ask about the menu or current deals.
    
    Context:
    {context}
    
    Question: {question}
    Answer:
    """

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user", "content":prompt}],
        temperature=0
    )
    return completion.choices[0].message.content
