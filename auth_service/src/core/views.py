from flask import Blueprint, render_template
from flask_security import (
    auth_required,
)

views = Blueprint('views', __name__)


# Views
@views.route('/')
@auth_required()
def index() -> str:
    return render_template('index.html')


# Views
@views.route('/profile')
@auth_required()
def profile() -> str:
    return render_template('profile.html')
