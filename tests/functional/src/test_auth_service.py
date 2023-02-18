from http import HTTPStatus

import pytest

from functional.settings import TestSettings

settings = TestSettings()


class BaseData:
    name = 'test'
    email = 'test3@me.com'
    password = 'password3'
    signup_data = {
        'name': name,
        'email': email,
        'password': password,
    }
    login_data = {
        'email': email,
        'password': password,
    }
    invalid_login_data = {
        'email': email,
        'password': 'invalid',
    }


def test_sign_up(make_post_request):
    response = make_post_request('/auth/register', data=BaseData.signup_data)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'data, status',
    [
        (BaseData.login_data, HTTPStatus.OK),
        (BaseData.invalid_login_data, HTTPStatus.UNAUTHORIZED),
    ],
)
def test_login(data, status, make_post_request):
    response = make_post_request('/auth/login', data)
    assert response.status_code == status


def test_logout(make_post_request):
    response = make_post_request('/auth/login', BaseData.login_data)
    assert response.status_code == HTTPStatus.OK

    logout = make_post_request('/auth/logout', BaseData.login_data)
    assert logout.status_code == 200


def test_logout_all(make_post_request):
    response = make_post_request('/auth/login', BaseData.login_data)
    assert response.status_code == HTTPStatus.OK

    logout = make_post_request('/auth/logout_all', BaseData.login_data)
    assert logout.status_code == 200
