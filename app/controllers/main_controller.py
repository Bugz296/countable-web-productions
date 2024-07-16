import os
from flask import Blueprint, request, current_app
from app.helpers.main_helper import get_hit_count

main_bp = Blueprint('main', __name__)
def hello():
    count = get_hit_count()
    return 'Hello from Docker! I have been seen {} times.\n'.format(count)

# Route for simulating the app stop to trigger the cronjob script for sending email notification that the app is down.
def simulate_app_stop():

    # Set is_stop_key value to 1.
    current_app.redis.set(current_app.redis_keys["is_stop_key"], 1)
    
    # Set is_delay_key value to 0 to avoid conflict.
    current_app.redis.set(current_app.redis_keys["is_delay_key"], 0)

    return 'WARNING: Any succeeding requests will return "HTTP ERROR 500".'

# Route for simulating the app to start. This is used after simulating the app is down.
def simulate_app_start():

    # Set is_stop_key value to 0.
    current_app.redis.set(current_app.redis_keys["is_stop_key"], 0)

    return 'INFO: The app has successfully started.'

# Route for simulating the app to intentionally delay the response time.
def simulate_app_delay():

    # Get the query parameter - "delay". Set default value if not set.
    delay = request.args.get('delay', default = os.getenv('DEFAULT_DELAY_SECONDS'), type = int)

    # Set cache is_delay value to 11 or n seconds
    current_app.redis.set(current_app.redis_keys["is_delay_key"], delay)

    # Set is_stop_key value to 0.
    current_app.redis.set(current_app.redis_keys["is_stop_key"], 0)

    return 'WARNING: All requests moving forward are now delayed {} seconds.'.format(delay)

# Route for removing the app delay. This is used after simulating the delayed response of the app.
def simulate_app_remove_delay():

    # Set cache is_delay value to 0 seconds
    current_app.redis.set(current_app.redis_keys["is_delay_key"], 0)

    return 'INFO: You should NO longer be receiving notifications via email about app running out of space in every minute.'