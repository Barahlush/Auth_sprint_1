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
    verify_jwt_in_request,
)
from flask_peewee.utils import object_list  # type: ignore
from flask_wtf.csrf import generate_csrf  # type: ignore
from loguru import logger

from src.core.jwt import (
    create_token_pair,
    revoke_all_user_tokens,
    revoke_token,
    roles_required,
    set_token_cookies,
)
from src.core.models import LoginEvent
from src.core.security import check_password, generate_salt, hash_password
from src.db.datastore import datastore
from src.utils.template_utils import navbar_items

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
    remember_me = request.form.get('remember', False)
    if not email or not password:
        error_msg = 'Enter the username and the password'
        return make_response(
            render_template('security/login_user.html', error_msg=error_msg),
            401,
        )

    user = datastore.find_user(email=email)

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
        user=user,
    )
    user_history.save()
    logger.info('user_history: %s', user_history)
    next_url = request.args.get('next', url_for('views.index'))
    response = cast(Response, redirect(next_url))

    access_token, refresh_token = create_token_pair(user)
    set_token_cookies(
        response, access_token, refresh_token, remember=remember_me
    )

    return response


@views.route('/change_login', methods=['GET', 'POST'])
@jwt_required()  # type: ignore
def change_login() -> Response:
    if request.method == 'GET':
        next_url = request.args.get('next', url_for('views.index'))
        return make_response(
            render_template(
                'security/change_login.html',
                next_url=url_for('views.change_login', next=next_url),
            ),
            200,
        )
    if not request.form:
        error_msg = 'Empty request'
        return make_response(
            render_template('security/change_login.html', error_msg=error_msg),
            401,
        )
    new_name = request.form.get('new_name', None)
    user = get_current_user()
    user.name = new_name
    user.save()
    logger.info('name %s %s', new_name, user)
    if not new_name or not user:
        error_msg = 'Can`t find a user or empty new name'
        return make_response(
            render_template('security/change_login.html', error_msg=error_msg),
            401,
        )
    logger.info(
        'Success login change. New login %s. User %s', new_name, user.id
    )
    next_url = request.args.get('next', url_for('views.index'))
    response = cast(Response, redirect(next_url))
    access_token, refresh_token = create_token_pair(user)
    set_token_cookies(response, access_token, refresh_token)
    return response


@views.route('/change_password', methods=['GET', 'POST'])
@jwt_required()  # type: ignore
def change_password() -> Response:
    if request.method == 'GET':
        next_url = request.args.get('next', url_for('views.index'))
        return make_response(
            render_template(
                'security/change_password.html',
                next_url=url_for('views.change_password', next=next_url),
            ),
            200,
        )
    if not request.form:
        error_msg = 'Empty request'
        return make_response(
            render_template(
                'security/change_password.html', error_msg=error_msg
            ),
            401,
        )
    new_password = request.form.get('new_password', None)
    user = get_current_user()
    salt = generate_salt()
    new_password_hash = hash_password(new_password, salt)  # type: ignore
    user.password = new_password_hash
    user.save()
    logger.info('new_password %s %s', new_password, user)
    if not new_password or not user:
        error_msg = 'Can`t find a user or empty new password'
        return make_response(
            render_template(
                'security/change_password.html', error_msg=error_msg
            ),
            401,
        )
    logger.info('Success password change for %s', user.id)
    next_url = request.args.get('next', url_for('views.index'))
    return cast(Response, redirect(next_url))


@views.route('/logout', methods=['POST'])
@roles_required('user', 'admin')
def logout() -> Response:
    response = make_response(redirect(url_for('views.login')), 302)

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
@roles_required('user', 'admin')
def logout_all() -> Response:
    response = make_response(redirect(url_for('views.login')), 302)
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

    if not username or not email or not password:
        error_msg = 'Enter the username and the password'
        return make_response(
            render_template('security/login_user.html', error_msg=error_msg),
            401,
        )

    salt = generate_salt()
    password_hash = hash_password(password, salt)
    datastore.create_user(
        name=username,
        email=email,
        password_hash=password_hash,
        fs_uniquifier=salt,
        roles=['user'],
    )
    next_url = request.args.get('next', url_for('views.index'))
    return make_response(
        redirect(url_for('views.login', next=next_url)),
        302,
    )


@views.route('/history')
@roles_required('user', 'admin')
def history() -> Response:
    current_user = get_current_user()
    user_history = (
        LoginEvent.select()  # type: ignore
        .where(LoginEvent.user == current_user)
        .order_by(LoginEvent.registered)
    )
    return make_response(
        object_list('security/history.html', user_history, paginate_by=10),
        200,
    )


@views.route('/')
@roles_required('user', 'admin')
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
@roles_required('user', 'admin')
def profile() -> Response:
    current_user = get_current_user()
    return make_response(
        render_template('security/profile.html', current_user=current_user),
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

    if refresh_token := request.cookies.get('refresh_token_cookie'):
        revoke_token(refresh_token)

    access_token, refresh_token = create_token_pair(current_user)
    set_token_cookies(response, access_token, refresh_token)
    return response


@views.context_processor
def inject_navbar() -> dict[str, list[str]]:
    verify_jwt_in_request(optional=True)
    current_user = get_current_user()
    csrf_token = generate_csrf()

    navbar = []
    if not current_user:
        logger.info('ANONIM')
        for item in navbar_items:
            item.init()
            if 'anon' in item.roles:
                is_active = item.href == request.path
                navbar.append(item.to_html(csrf_token, is_active))
        return {'navbar_items': navbar}
    logger.info('AUTHORIZED')
    for item in navbar_items:
        item.init()
        for role in current_user.roles:
            if role.name in item.roles:
                is_active = item.href == request.path
                navbar.append(item.to_html(csrf_token, is_active))
    return {'navbar_items': navbar}
