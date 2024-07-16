
from flask import Blueprint, current_app
from app.helpers.main_helper import get_hit_count

main_bp = Blueprint('main', __name__)
def hello():
    count = get_hit_count()
    return 'Hello from Docker! I have been seen {} times.\n'.format(count)

# Route for simulating the app stop to trigger the cronjob script for sending email notification that the app is down.
def simulate_app_stop():

    # Set is_stop_key value to 1.
    current_app.redis.set(current_app.redis_keys["is_stop_key"], 1)

    return 'WARNING: Any succeeding requests will return "HTTP ERROR 500".'

# Route for simulating the app to start. This is used after simulating the app is down.
def simulate_app_start():

    # Set is_stop_key value to 0.
    current_app.redis.set(current_app.redis_keys["is_stop_key"], 0)

    return 'INFO: The app has successfully started.'