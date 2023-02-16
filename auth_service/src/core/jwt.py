from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, cast

from flask import Response, redirect, request, url_for
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt,
    verify_jwt_in_request,
)
from flask_jwt_extended.exceptions import JWTExtendedException
from loguru import logger

from src.core.models import User

jwt = JWTManager()
P = ParamSpec('P')


def roles_required(
    *roles: str,
) -> Callable[[Callable[P, Response]], Callable[P, Response]]:
    """Параметризованный декоратор для проверки роли пользователя

    Args:
        role (str): Роль пользователя

    Usage:
        @views.route('/admin')
        @role_required('admin')
        def admin() -> str:
            ...
    """

    def wrapper(fn: Callable[P, Response]) -> Callable[P, Response]:
        """A decorator

        Args:
            fn (Callable[P, Response]):

        Returns:
            Callable[P, Response]:
        """

        @wraps(fn)
        def decorated_view(*args: P.args, **kwargs: P.kwargs) -> Response:
            try:
                verify_jwt_in_request()
                claims = get_jwt()

                if len(roles) == 0:
                    return fn(*args, **kwargs)

                for role in claims['roles']:
                    if role in roles:
                        return fn(*args, **kwargs)
            except JWTExtendedException:
                logger.info(
                    'Failed to validate jwt and/or role: {claims}',
                    claims=claims,
                )
            return cast(
                Response,
                redirect(
                    url_for('views.login', next=request.path),
                ),
            )

        return decorated_view

    return wrapper


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> int:
    return int(user.id)  # type: ignore


@jwt.unauthorized_loader
def unauthorized_callback(_: str) -> Response:
    return cast(
        Response,
        redirect(
            url_for('views.login', next=request.path),
        ),
    )


@jwt.user_lookup_loader
def user_lookup_callback(
    _jwt_header: dict[str, str | int], jwt_data: dict[str, str | int]
) -> User:
    identity = int(jwt_data['sub'])
    return cast(User, User.get_by_id(identity))   # type: ignore


@jwt.expired_token_loader
def expired_token_callback(
    _jwt_header: dict[str, str | int], jwt_data: dict[str, str | int]
) -> Response:
    """Вызывается при истечении срока действия одного из токенов.

    При истечении срока действия refresh токена, происходит редирект на
    страницу логина.

    При истечении срока действия access токена, происходит редирект на
    /refresh и затем на искомую страницу.

    Args:
        _jwt_header (dict[str, str  |  int]): заголовок токена
        jwt_data (dict[str, str  |  int]): payload токена

    Returns:
        Response: Ответ браузеру
    """
    logger.info('TOKEN EXPIRED')
    logger.info(request.path)
    logger.info(jwt_data)
    token_type = jwt_data['type']

    if token_type == 'refresh':   # noqa
        return cast(
            Response,
            redirect(
                url_for('views.login', next=request.path),
            ),
        )
    refresh_token = request.cookies.get('refresh_token_cookie')
    if not refresh_token:
        return cast(
            Response,
            redirect(
                url_for('views.login', next=request.path),
            ),
        )

    return cast(
        Response,
        redirect(
            url_for('views.refresh', next=request.path),
        ),
    )


def create_token_pair(user: User) -> tuple[str, str]:
    """Создание закодированной пары токенов

    Args:
        user (User): Пользователь

    Returns:
        tuple[str, str]: Пара токенов
    """
    access_token = create_access_token(
        identity=user,
        additional_claims={
            'roles': [role.name for role in user.roles]  # type: ignore
        },
    )
    refresh_token = create_refresh_token(identity=user)
    return access_token, refresh_token
