from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()  # Initialize SocketIO here

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.Config')
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    # Initialize SocketIO with the app
    socketio.init_app(app)
    
    return app