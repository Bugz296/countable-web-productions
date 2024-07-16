import time
from flask import current_app

# Set keys for redis
is_stop_key = "is_stopped"

# middleware.py
class CustomMiddleware:
    def __init__(self, app, redis_client):
        self.app = app
        self.redis_client = redis_client

    def __call__(self, environ, start_response):

        start_time = time.time()

        # Code to run before the request
        print("Before Request")
        
        def custom_start_response(status, headers, exc_info=None):
            with current_app.app_context():
                end_time = time.time()
                print("Request finished")
                print(f"Time taken: {end_time - start_time:.4f} seconds")

                # Get the value from redis if simulation for app being stopped is active or not.
                is_app_stopped = int(self.redis_client.get(is_stop_key) if self.redis_client.get(is_stop_key) is not None else 0)

                # Proceed if is_stop_key is set to 1.
                if is_app_stopped == 1:

                    # Set response status to 500 Internal Server Error
                    status = '500 INTERNAL SERVER ERROR'

                return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)