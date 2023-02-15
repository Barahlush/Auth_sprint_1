from flask import render_template
from flask_jwt_extended import get_current_user, jwt_required
from main import app


@app.route('/')
@jwt_required()  # type: ignore
def index() -> str:
    welcome_string = 'Welcome!'
    current_user = get_current_user()
    contex = {}
    if current_user:
        contex.update({'user': current_user})
        if current_user.name:
            welcome_string = f'Welcome back, {current_user.name}!'
            contex.update({'"user_name': current_user.name})
        else:
            welcome_string = 'Welcome back!'
    contex.update({'welcome_string': welcome_string})
    if current_user.email:
        contex.update({'user_email': current_user.email})
    return render_template('index.html', contex=contex)
