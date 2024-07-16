
from flask import Blueprint
from app.helpers.main_helper import get_hit_count

main_bp = Blueprint('main', __name__)
def hello():
    count = get_hit_count()
    return 'Hello from Docker! I have been seen {} times.\n'.format(count)