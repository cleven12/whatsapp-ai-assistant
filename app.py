"""
Development entry point for WhatsApp AI Assistant.

For production use gunicorn (see Dockerfile):
    gunicorn --bind 0.0.0.0:5000 "app:create_app()"
"""
from app import create_app, db
from app.models import User, Message

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Flask shell helpers."""
    return {'db': db, 'User': User, 'Message': Message}

if __name__ == '__main__':
    app.run(debug=True)
