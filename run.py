import os
from app import create_app, socketio  # Import socketio from app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    socketio.run(app, host='127.0.0.1', port=port, debug=True)