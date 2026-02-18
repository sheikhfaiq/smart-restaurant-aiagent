import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.agent.tools.rag_tool import generate_answer

def test_rag():
    question = "i am talking about different type of sauce option"
    try:
        print(f"Testing RAG with question: {question}")
        answer = generate_answer(question)
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_rag()
