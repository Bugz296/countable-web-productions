from flask import current_app
import time

def get_hit_count():
    redis_client = current_app.redis
    redis_exceptions = current_app.redis_exceptions
    retries = 5
    while True:
        try:
            return redis_client.incr('hits')
        except redis_exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)