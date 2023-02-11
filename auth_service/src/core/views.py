from flask import Blueprint, app, flash, render_template_string, request
from flask_security import auth_required

views = Blueprint('views', __name__)


# Views
@views.route('/')
@auth_required()  # type: ignore
def home() -> str:
    return render_template_string('Film service home page')


@views.route('/profile')
@auth_required()  # type: ignore
def profile() -> str:
    return render_template_string('Hello {{ current_user.email }}')


@views.route('/roles/<name:str>', methods=['GET', 'POST', 'DELETE'])
@auth_required()  # type: ignore
def find_create_role():
    """
    Find, create or delete a Role record.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        return app.security.datastore.find_or_create_role(  # type: ignore
            name=name
        )
    if request.method == 'GET':
        return request.args.getlist('role')
    """
    Так удалять нехорошо. Не знаешь, как лучше сделать?
    # у security только delete_user
    # db.execute(f'Delete from role where name={request.form.get("name")}')
    # db.commit()
    """
    return flash('Role was deleted successfully')
