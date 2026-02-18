import os
import json
import psycopg2
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import OPENAI_API_KEY, DATABASE_URL
from app.services.rag.embedding import get_embedding

def ingest_documents():
    # 1. Connect to Supabase/PostgreSQL
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # 2. Ensure pgvector extension and table exist
    # Users need to have permissions to create extensions, usually standard on Supabase
    try:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id bigserial PRIMARY KEY,
                content text,
                embedding vector(1536),
                metadata jsonb
            );
        """)
        conn.commit()
    except Exception as e:
        print(f"Error setting up table: {e}")
        conn.rollback()

    # 3. Setup Text Splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # 4. Process each PDF in the docs folder
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        print(f"Directory {docs_dir} not found.")
        return

    for filename in os.listdir(docs_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(docs_dir, filename)
            print(f"Processing {filename}...")
            
            try:
                loader = PyPDFLoader(file_path)
                pages = loader.load()
                chunks = splitter.split_documents(pages)
                
                print(f"  Split into {len(chunks)} chunks. Generating embeddings...")
                
                for i, chunk in enumerate(chunks):
                    content = chunk.page_content
                    # Use our modular embedding utility
                    embedding = get_embedding(content)
                    
                    metadata = {
                        "source": filename,
                        "page": chunk.metadata.get("page", 0)
                    }
                    
                    cursor.execute(
                        """
                        INSERT INTO documents (content, embedding, metadata)
                        VALUES (%s, %s, %s)
                        """,
                        (content, embedding, json.dumps(metadata))
                    )
                    
                    if (i + 1) % 10 == 0:
                        print(f"    Progress: {i + 1}/{len(chunks)} chunks inserted.")
                
                conn.commit()
                print(f"Successfully ingested {filename}.")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                conn.rollback()

    cursor.close()
    conn.close()
    print("All documents ingested successfully! 🚀")

if __name__ == "__main__":
    ingest_documents()
