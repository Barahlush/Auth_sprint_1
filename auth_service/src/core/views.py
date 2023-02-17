from typing import cast

from flask import (
    Blueprint,
    Response,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import (
    get_current_user,
    jwt_required,
    unset_jwt_cookies,
)
from loguru import logger

from src.core.jwt import (
    create_token_pair,
    revoke_all_user_tokens,
    revoke_token,
    roles_required,
    set_token_cookies,
)
from src.core.models import User

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

    next_url = request.args.get('next', url_for('views.index'))
    response = cast(Response, redirect(next_url))

    access_token, refresh_token = create_token_pair(user)
    set_token_cookies(response, access_token, refresh_token)

    return response


@views.route('/logout', methods=['POST'])
@jwt_required()  # type: ignore
def logout() -> Response:
    response = make_response(redirect(url_for('views.login')))

    # Отзыв access токена
    if access_token := request.cookies.get('access_token_cookie'):
        revoke_token(access_token)

    # Отзыв refresh токена
    if refresh_token := request.cookies.get('refresh_token_cookie'):
        revoke_token(refresh_token)
    logger.info('REVOKING TOKEN')
    unset_jwt_cookies(response)

    return response


@views.route('/logout_all', methods=['POST'])
@jwt_required()  # type: ignore
def logout_all() -> Response:
    response = make_response(redirect(url_for('views.login')))
    logger.info('REVOKING ALL TOKENS')
    current_user = get_current_user()
    revoke_all_user_tokens(current_user)
    unset_jwt_cookies(response)
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
    set_token_cookies(response, access_token, refresh_token)

    return response


@views.route('/admin')
@roles_required('admin')
def admin() -> Response:
    current_user = get_current_user()
    return make_response(
        render_template(
            f'Hello on admin page. Current user '
            f'{current_user.email} password is {current_user.password}'
        ),
        200,
    )


@views.route('/test')
@jwt_required()  # type: ignore
def test_page() -> Response:
    current_user = get_current_user()
    return make_response(
        render_template('Hello on test page.' f'Current user {current_user}'),
        200,
    )


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
    set_token_cookies(response, access_token, refresh_token)
    return response


@views.route('/')
@jwt_required()  # type: ignore
def index() -> Response:
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
    return make_response(
        render_template('security/index.html', contex=contex), 200
    )


@views.route('/profile')
@jwt_required()  # type: ignore
def profile() -> Response:
    current_user = get_current_user()
    return make_response(
        render_template('security/profile.html', current_user=current_user),
        200,
    )
