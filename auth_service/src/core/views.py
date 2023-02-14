from flask import Blueprint, render_template, render_template_string
from flask_security import auth_required, current_user, permissions_accepted

views = Blueprint('views', __name__)


@views.route('/admin')
@auth_required()
@permissions_accepted('admin-read', 'admin-write')
def admin() -> str:
    return render_template_string(
        f'Hello on admin page. Current user '
        f'{current_user.email} password is {current_user.password}'
    )


@views.route('/')
@auth_required()
def index() -> str:
    return render_template('security/index.html')
