from flask import Blueprint, render_template_string
from flask_security import (
    auth_required,
)

views = Blueprint('views', __name__)

# Views
@views.route('/')
@auth_required()
def home() -> str:
    return render_template_string('Film service home page')


@views.route('/profile')
@auth_required()
def profile() -> str:
    return render_template_string('Hello {{ current_user.email }}')
