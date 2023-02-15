from flask import render_template
from main import app
from src.core.views import ResponseType


@app.route('/')
def index() -> ResponseType:
    return render_template('index.html'), 200
