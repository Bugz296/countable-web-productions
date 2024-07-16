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
        # Set the prev_is_app_stopped value to the value from redis.
        # This is used for letting the user know if the request for stopping the app is successful.
        prev_is_app_stopped = int(self.redis_client.get(is_stop_key) if self.redis_client.get(is_stop_key) is not None else 0)


        # Code to run before the request
        print("Before Request", prev_is_app_stopped)
        
        def custom_start_response(status, headers, exc_info=None):
            with current_app.app_context():
                end_time = time.time()
                print("Request finished")
                print(f"Time taken: {end_time - start_time:.4f} seconds")
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)
