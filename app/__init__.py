# app/__init__.py
from flask import Flask
from redis import Redis, exceptions
from dotenv import load_dotenv
import os
from app.routes.main_routes import main_bp

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Initialize Redis client
    redis_client = Redis(
        host                = os.getenv('REDIS_HOST'),
        port                = os.getenv('REDIS_PORT'),
        decode_responses    = os.getenv('REDIS_DECODE_RESPONSES') == 'True'
    )

    app.redis_exceptions = exceptions

    # Add the Redis client to the app context
    app.redis = redis_client

    # Register blueprints
    app.register_blueprint(main_bp)

    return app