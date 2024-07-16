import time
from flask import current_app, request

# middleware.py
class CustomMiddleware:
    def __init__(self, app, redis_client):
        self.app = app
        self.redis_client = redis_client

    def __call__(self, environ, start_response):

        # Code to run before the request
        print("Before Request")

        start_time = time.time()
        
        def custom_start_response(status, headers, exc_info=None):
            with current_app.app_context():
                
                # Get the value of delay from redis, if not yet set, default value is 0.
                delay = int(self.redis_client.get(current_app.redis_keys["is_delay_key"]) if self.redis_client.get(current_app.redis_keys["is_delay_key"]) is not None else 0)

                # Proceed if delay value is set more than 0 seconds and request is not from the list = ['/simulate_app_remove_delay', '/reset'].
                if delay > 0 and request.path not in ['/simulate_app_remove_delay']:

                    # Set is_stop_key value to 0, so that the simulation for delayed app will not conflict with simulation for stopped app.
                    current_app.redis.set(current_app.redis_keys["is_stop_key"], 0)

                    # Call function to delay process.
                    time.sleep(delay)

                end_time = time.time()
                elapsed_time = int(end_time - start_time)

                print("Request finished")
                print(f"Time taken: {end_time - start_time:.4f} seconds")

                # Get the value from redis if simulation for app being stopped is active or not.
                is_app_stopped = int(self.redis_client.get(current_app.redis_keys["is_stop_key"]) if self.redis_client.get(current_app.redis_keys["is_stop_key"]) is not None else 0)

                # Proceed if is_stop_key is set to 1.
                if is_app_stopped == 1:

                    # Set response status to 500 Internal Server Error
                    status = '500 INTERNAL SERVER ERROR'

                # Proceed elapsed_time is more than 10 seconds
                elif elapsed_time > 10:

                    # Set response status to 408 Request Timeout
                    status = '408 Request Timeout'
                return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)