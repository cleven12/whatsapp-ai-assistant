from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
import logging

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Application factory for WhatsApp AI Assistant."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Setup basic logging
    logging.basicConfig(
        level=getattr(logging, app.config.get('LOG_LEVEL', 'INFO')),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from .routes.webhook import webhook_bp
    from .routes.dashboard import dashboard_bp
    
    app.register_blueprint(webhook_bp, url_prefix='/webhook')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # Simple health check
    @app.route('/health')
    def health():
        return {"status": "ok", "service": "whatsapp-ai-assistant"}, 200

    return app
