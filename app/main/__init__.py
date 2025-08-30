from flask import Blueprint

# Create main blueprint
bp = Blueprint('main', __name__)

# Import routes at the bottom to avoid circular imports
from . import routes
