from flask import Blueprint

# Create a Blueprint for user-related routes
user_bp = Blueprint('user', __name__)

# Import routes at the bottom to avoid circular imports
from app.user import routes
