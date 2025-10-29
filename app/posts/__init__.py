from flask import Blueprint

# Create the main posts blueprint
posts_bp = Blueprint('posts', __name__)

# Import routes at the bottom to avoid circular imports
from . import routes, likes  # noqa
