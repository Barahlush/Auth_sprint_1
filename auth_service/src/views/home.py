from flask import Blueprint, render_template_string
from flask_security import (
    auth_required,
)
from src.app import app

my_view = Blueprint('home', __name__)

# Views
@app.route('/')
@auth_required()
def home() -> str:
    return render_template_string('Hello {{ current_user.email }}')
