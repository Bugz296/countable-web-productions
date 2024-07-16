# app/routes/main.py
from flask import Blueprint
from app.controllers.main_controller import hello

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return hello()
