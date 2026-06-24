"""
Pinecone index setup helper.

Run once before ingesting documents:
    python setup_pinecone.py
"""
import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

def setup_pinecone():
    """Create the Pinecone index if it does not exist (matches embedding dim)."""
    api_key = os.getenv('PINECONE_API_KEY')
    index_name = os.getenv('PINECONE_INDEX_NAME', 'whatsapp-rag')
    
    if not api_key:
        print("Error: PINECONE_API_KEY missing.")
        return

    pc = Pinecone(api_key=api_key)
    indexes = [idx.name for idx in pc.list_indexes()]

    if index_name not in indexes:
        print(f"Creating index '{index_name}' ...")
        try:
            pc.create_index(
                name=index_name,
                dimension=384,  # all-MiniLM-L6-v2
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
            print(f"Index creation started for '{index_name}'.")
            
            # Poll readiness
            while True:
                status = pc.describe_index(index_name).status
                if status.get('ready'):
                    break
                print("Waiting for index to become ready...")
                time.sleep(2)
            print(f"✅ Index '{index_name}' is ready!")
        except Exception as e:
            print(f"Error creating index: {e}")
    else:
        print(f"Index '{index_name}' already exists. Nothing to do.")

if __name__ == "__main__":
    setup_pinecone()
