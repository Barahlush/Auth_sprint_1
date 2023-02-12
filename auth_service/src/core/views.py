from flask import Blueprint, render_template
from flask_security import (
    auth_required,
)

views = Blueprint('views', __name__)


# Views
@views.route('/')
@auth_required()
def home() -> str:
    return render_template('security/index.html')
