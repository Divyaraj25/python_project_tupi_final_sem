from flask import Blueprint

# Create main blueprint
main = Blueprint('main', __name__)

# Import routes after creating the blueprint to avoid circular imports
from app.main import routes
