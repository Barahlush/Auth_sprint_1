from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, cast

from flask import (
    Blueprint,
    Response,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_current_user,
    get_jwt,
    jwt_required,
    set_access_cookies,
    verify_jwt_in_request,
)
from loguru import logger
from werkzeug import Response as WerkzeugResponse

from src.core.models import User

P = ParamSpec('P')
ResponseType = tuple[WerkzeugResponse | Response | str, int]


def roles_required(
    *roles: str,
) -> Callable[[Callable[P, ResponseType]], Callable[P, ResponseType]]:
    """Параметризованный декоратор для проверки роли пользователя

    Args:
        role (str): Роль пользователя

    Usage:
        @views.route('/admin')
        @role_required('admin')
        def admin() -> str:
            ...
    """

    def wrapper(fn: Callable[P, ResponseType]) -> Callable[P, ResponseType]:
        @wraps(fn)
        def decorated_view(*args: P.args, **kwargs: P.kwargs) -> ResponseType:
            verify_jwt_in_request()
            claims = get_jwt()
            logger.info(claims)
            logger.info(roles)
            for role in claims['roles']:
                if role in roles:
                    return fn(*args, **kwargs)
            return (
                redirect(url_for('views.login', next=request.path)),
                302,
            )

        return decorated_view

    return wrapper


views = Blueprint('views', __name__)
jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> int:
    return int(user.id)  # type: ignore


@jwt.user_lookup_loader
def user_lookup_callback(
    _jwt_header: dict[str, str | int], jwt_data: dict[str, str | int]
) -> User:
    identity = int(jwt_data['sub'])
    return cast(User, User.get_by_id(identity))   # type: ignore


@views.route('/login', methods=['GET', 'POST'])
def login() -> ResponseType:
    if request.method == 'GET':
        next_url = request.args.get('next', url_for('views.index'))
        return (
            render_template(
                'security/login_user.html',
                next_url=url_for('views.login', next=next_url),
            ),
            200,
        )
    if not request.form:
        return jsonify('Empty request'), 401
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if not email or not password:
        return jsonify('Enter the username and the password'), 401

    user: User = User.get(email=email)   # type: ignore

    def check_password(user: User, password: str) -> bool:
        """Небезопасная проверка пароля"""
        logger.info(user.password)
        logger.info(password)
        return bool(user.password == password)

    if not user or not check_password(user, password):
        return jsonify('Wrong username or password'), 401

    access_token = create_access_token(
        identity=user,
        additional_claims={
            'roles': [role.name for role in user.roles]  # type: ignore
        },
    )
    next_url = request.args.get('next', url_for('views.index'))
    response = redirect(next_url, 302)
    set_access_cookies(response, access_token)   # type: ignore
    return response, 302


@views.route('/register', methods=['GET', 'POST'])
def register() -> ResponseType:
    if request.method == 'GET':
        return render_template('security/register_user.html'), 200
    if not request.form:
        return jsonify('Empty request'), 401
    username = request.form.get('name', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    user = User(name=username, email=email, password=password)
    user.save()
    access_token = create_access_token(
        identity=user,
        additional_claims={
            'roles': [role.name for role in user.roles]  # type: ignore
        },
    )
    next_url = request.args.get('next', url_for('views.index'))
    response = redirect(next_url, 302)
    set_access_cookies(response, access_token)  # type: ignore
    return response, 302


@views.route('/')
@jwt_required()  # type: ignore
def index() -> ResponseType:
    welcome_string = 'Welcome!'
    current_user = get_current_user()
    contex = {}
    if current_user:
        contex.update({'user': current_user})
        try:
            name = current_user.name
            email = current_user.email
            contex.update({'"user_name': name})
            contex.update({'user_email': email})
            welcome_string = f'Welcome back, {current_user.name}!'
        except AttributeError:
            welcome_string = 'Welcome back!'
    contex.update({'welcome_string': welcome_string})
    return render_template('security/index.html', contex=contex), 200


@views.route('/profile')
@jwt_required()  # type: ignore
def profile() -> ResponseType:
    current_user = get_current_user()
    response = render_template(
        'security/profile.html', current_user=current_user
    )
    return response, 200
