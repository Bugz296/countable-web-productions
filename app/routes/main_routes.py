# app/routes/main.py
from flask import Blueprint
from app.controllers.main_controller import hello, simulate_app_stop, simulate_app_start

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return hello()

@main_bp.route('/simulate_app_stop')
def stop():
    return simulate_app_stop()


@main_bp.route('/simulate_app_start')
def start():
    return simulate_app_start()