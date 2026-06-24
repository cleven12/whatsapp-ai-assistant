from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore as LangChainPinecone
from langchain_huggingface import HuggingFaceEmbeddings
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class RAGService:
    """Retrieval-Augmented Generation service backed by Pinecone."""

    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    def __init__(self):
        cfg = current_app.config
        self.api_key = cfg['PINECONE_API_KEY']
        self.index_name = cfg['PINECONE_INDEX_NAME']
        self.top_k = cfg.get('RAG_TOP_K', 3)
        
        self.embeddings = HuggingFaceEmbeddings(model_name=self.EMBEDDING_MODEL)
        
        self.pc = Pinecone(api_key=self.api_key)
        self.index = self.pc.Index(self.index_name)

    def query(self, text, k=None):
        """
        Retrieve top-k most relevant document chunks for the query text.
        """
        k = k or self.top_k
        try:
            vectorstore = LangChainPinecone(
                self.index, 
                self.embeddings, 
                "text"
            )
            docs = vectorstore.similarity_search(text, k=k)
            context = "\n".join([doc.page_content for doc in docs])
            logger.debug(f"RAG returned {len(docs)} chunks")
            return context
        except Exception as e:
            logger.error(f"Error querying Pinecone: {e}")
            return ""
