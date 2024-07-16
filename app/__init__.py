# app/__init__.py
from flask import Flask
from redis import Redis, exceptions
from dotenv import load_dotenv
import os
from app.routes.main_routes import main_bp
from app.middlewares.main_middleware import CustomMiddleware

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

    # Holds keys of configurations available in Redis.
    app.redis_keys = {
        "is_stop_key": "is_stopped",
        "is_delay_key": "is_delayed"
    }

    app.redis_exceptions = exceptions

    # Add the Redis client to the app context
    app.redis = redis_client

    # Apply the middleware
    app.wsgi_app = CustomMiddleware(app.wsgi_app, redis_client)

    # Register blueprints
    app.register_blueprint(main_bp)

    return app