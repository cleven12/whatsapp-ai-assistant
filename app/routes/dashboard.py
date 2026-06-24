from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Professional dashboard page (Free + Pro highlights)."""
    return render_template('dashboard.html')
