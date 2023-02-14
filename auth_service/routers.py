from flask import render_template
from flask_security import auth_required
from main import app


@app.route('/')
@auth_required()
def index() -> str:
    return render_template('index.html')
