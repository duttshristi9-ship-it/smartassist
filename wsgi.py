import os
from app import create_app

# Create the application instance
app = create_app(os.environ.get('FLASK_ENV', 'production'))

if __name__ == "__main__":
    from extensions import socketio
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
