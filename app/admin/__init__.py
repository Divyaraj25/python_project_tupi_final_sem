from flask import Blueprint

# Create admin blueprint
bp = Blueprint('admin', __name__)

# Import routes at the bottom to avoid circular imports
from . import routes
