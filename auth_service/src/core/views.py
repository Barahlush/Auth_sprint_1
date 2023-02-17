from typing import cast

from flask import (
    Blueprint,
    Response,
    make_response,
    redirect,
    render_template,
    render_template_string,
    request,
    url_for,
)
from flask_jwt_extended import (
    get_current_user,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
)
from loguru import logger

from src.core.jwt import create_token_pair, roles_required
from src.core.models import LoginEvent, User

views = Blueprint('views', __name__, url_prefix='/auth')


@views.route('/login', methods=['GET', 'POST'])
def login() -> Response:
    if request.method == 'GET':
        next_url = request.args.get('next', url_for('views.index'))
        return make_response(
            render_template(
                'security/login_user.html',
                next_url=url_for('views.login', next=next_url),
            ),
            200,
        )
    if not request.form:
        error_msg = 'Empty request'
        return make_response(
            render_template('security/login_user.html', error_msg=error_msg),
            401,
        )
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if not email or not password:
        error_msg = 'Enter the username and the password'
        return make_response(
            render_template('security/login_user.html', error_msg=error_msg),
            401,
        )

    user: User = User.get(email=email)   # type: ignore

    def check_password(user: User, password: str) -> bool:
        """Небезопасная проверка пароля"""
        logger.info(user.password)
        logger.info(password)
        return bool(user.password == password)

    if not user or not check_password(user, password):
        error_msg = 'Wrong username or password'
        return make_response(
            render_template('security/login_user.html', error_msg=error_msg),
            401,
        )
    history = request.headers.get('User-Agent')
    logger.info(history)
    user_history = LoginEvent(
        history=history,
        user=User.get(id=user),  # type: ignore
    )
    user_history.save()
    logger.info(f'user_history: {user_history}')
    next_url = request.args.get('next', url_for('views.index'))
    response = cast(Response, redirect(next_url))

    access_token, refresh_token = create_token_pair(user)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@views.route('/register', methods=['GET', 'POST'])
def register() -> Response:
    if request.method == 'GET':
        return make_response(
            render_template('security/register_user.html'), 200
        )
    if not request.form:
        error_msg = 'Empty request'
        return make_response(
            render_template('security/login_user.html', error_msg=error_msg),
            401,
        )
    username = request.form.get('name', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    user = User(name=username, email=email, password=password)
    user.save()
    next_url = request.args.get('next', url_for('views.index'))
    response = cast(Response, redirect(next_url, 302))

    access_token, refresh_token = create_token_pair(user)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, access_token)

    return response


@views.route('/admin')
@roles_required('admin')
def admin() -> Response:
    current_user = get_current_user()
    return make_response(
        render_template_string(
            f'Hello on admin page. Current user '
            f'{current_user.email} password is {current_user.password}'
        ),
        200,
    )


@views.route('/history')
@jwt_required()  # type: ignore
def test_page() -> Response:
    current_user = get_current_user()
    user_history = (
        LoginEvent.select()  # type: ignore
        .where(LoginEvent.user == current_user)
        .order_by(LoginEvent.registered)
        .limit(10)
    )
    return make_response(
        render_template('security/history.html', user_history=user_history),
        401,
    )


@views.route('/')
def index() -> Response:
    return make_response(render_template('security/index.html'), 200)


@views.route('/refresh')
@jwt_required(refresh=True)   # type: ignore
def refresh() -> Response:
    """Генерирует новую пару токенов, если refresh токен не истёк.
    Иначе, вызывает expired_token_callback и перенаправляет на страницу логина.

    Returns:
        Response: Ответ браузеру
    """
    current_user = get_current_user()
    next_url = request.args.get('next', url_for('views.index'))
    response = cast(Response, redirect(next_url, 302))

    access_token, refresh_token = create_token_pair(current_user)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response
