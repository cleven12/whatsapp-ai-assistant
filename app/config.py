import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class for the WhatsApp AI Assistant."""
    
    VERSION = "1.0.0"
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-123')
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    basedir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(basedir)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('sqlite:///instance/'):
        db_file = SQLALCHEMY_DATABASE_URI.replace('sqlite:///instance/', '')
        db_path = os.path.join(project_root, 'instance', db_file)
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    elif not SQLALCHEMY_DATABASE_URI:
        db_path = os.path.join(project_root, 'instance', 'database.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # WhatsApp Cloud API
    WHATSAPP_TOKEN = os.environ.get('WHATSAPP_TOKEN')
    WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
    WHATSAPP_VERIFY_TOKEN = os.environ.get('WHATSAPP_VERIFY_TOKEN')
    
    # LLM API Keys (LLMRouter will pick first available)
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    XAI_API_KEY = os.environ.get('XAI_API_KEY')
    
    # Pinecone
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENVIRONMENT')
    PINECONE_INDEX_NAME = os.environ.get('PINECONE_INDEX_NAME', 'whatsapp-rag')

    # RAG Settings
    RAG_TOP_K = int(os.environ.get('RAG_TOP_K', '3'))
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', '1000'))
