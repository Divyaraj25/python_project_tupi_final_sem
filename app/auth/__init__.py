from flask import Blueprint

# Create auth blueprint
bp = Blueprint('auth', __name__)

# Import routes at the bottom to avoid circular imports
from . import routes
