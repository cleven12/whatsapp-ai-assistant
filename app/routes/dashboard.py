from flask import Blueprint, render_template, current_app

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Professional dashboard page (Free + Pro highlights)."""
    return render_template(
        'dashboard.html',
        version=current_app.config.get('VERSION', '0.2.0')
    )
