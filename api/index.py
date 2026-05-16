import os
import sys

# Add the parent directory to sys.path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Vercel entrypoint requires the app object to be named 'app'
app = create_app(os.environ.get('FLASK_ENV', 'production'))
