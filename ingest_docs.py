"""
Knowledge base ingestion script.

Usage:
    python ingest_docs.py

Place your documents in the `uploads/` folder (txt/pdf supported).
"""
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

def ingest_docs():
    """Ingest documents from uploads/ into the configured Pinecone index."""
    api_key = os.getenv('PINECONE_API_KEY')
    index_name = os.getenv('PINECONE_INDEX_NAME', 'whatsapp-rag')
    chunk_size = int(os.getenv('CHUNK_SIZE', '1000'))
    
    if not api_key:
        print("Error: PINECONE_API_KEY not found in .env")
        return

    print(f"Starting ingestion to index: {index_name}...")

    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"Created '{uploads_dir}/' directory. Add .txt and .pdf files then rerun.")
        return

    # Load documents
    loader_txt = DirectoryLoader(uploads_dir + '/', glob="**/*.txt", loader_cls=TextLoader)
    loader_pdf = DirectoryLoader(uploads_dir + '/', glob="**/*.pdf", loader_cls=PyPDFLoader)
    
    docs = loader_txt.load() + loader_pdf.load()
    
    if not docs:
        print("No documents found in 'uploads/' directory.")
        return

    print(f"Loaded {len(docs)} documents.")

    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    try:
        pc = Pinecone(api_key=api_key)
        active_indexes = [index.name for index in pc.list_indexes()]
        
        if index_name not in active_indexes:
            print(f"Error: Index '{index_name}' does not exist.")
            print(f"Available: {active_indexes}")
            print("Run `python setup_pinecone.py` first.")
            return

        print("Uploading chunks to Pinecone...")
        PineconeVectorStore.from_documents(
            chunks,
            embeddings,
            index_name=index_name
        )
        print("✅ Successfully uploaded knowledge base to Pinecone!")

    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    ingest_docs()
