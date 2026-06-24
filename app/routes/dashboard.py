from flask import Blueprint, jsonify

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Basic dashboard placeholder. Ready to be expanded with real UI."""
    return jsonify({
        "message": "WhatsApp AI Assistant Dashboard",
        "status": "RAG Management coming soon",
        "endpoints": {
            "health": "/health",
            "webhook": "/webhook/"
        }
    })
