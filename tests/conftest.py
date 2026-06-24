import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret",
        "WHATSAPP_VERIFY_TOKEN": "test-verify",
        # Dummy keys so router doesn't explode in tests that don't hit LLM
        "GROQ_API_KEY": None,
        "PINECONE_API_KEY": "dummy",
        "PINECONE_INDEX_NAME": "test",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
