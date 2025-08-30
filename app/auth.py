from flask import Blueprint

# Create auth blueprint
auth = Blueprint('auth', __name__)

# Import routes after creating the blueprint to avoid circular imports
from app.auth import routes
