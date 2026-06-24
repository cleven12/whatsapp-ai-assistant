"""Route blueprints package."""
from .webhook import webhook_bp
from .dashboard import dashboard_bp

__all__ = ["webhook_bp", "dashboard_bp"]
