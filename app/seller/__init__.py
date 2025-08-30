from flask import Blueprint

# Create seller blueprint
bp = Blueprint('seller', __name__)

# Import routes at the bottom to avoid circular imports
from . import routes
