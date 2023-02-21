from http import HTTPStatus

import pytest

from functional.settings import TestSettings

settings = TestSettings()


class BaseData:
    name = 'test'
    email = 'test3@me.com'
    password = 'password3'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain',
        'Content-Encoding': 'utf-8',
    }
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


def test_get_history(make_get_request):
    response = make_get_request(
        '/auth/history', params=BaseData.login_data, headers=BaseData.headers
    )
    assert response.status_code == HTTPStatus.OK


def test_get_index(make_get_request):
    response = make_get_request(
        '', params=BaseData.login_data, headers=BaseData.headers
    )
    assert response.status_code == HTTPStatus.OK


def test_get_user_profile(make_get_request):
    response = make_get_request(
        '/auth/profile', params=BaseData.login_data, headers=BaseData.headers
    )
    assert response.status_code == HTTPStatus.OK


def test_get_refresh_token(make_get_request):
    response = make_get_request(
        '/auth/refresh', params=BaseData.login_data, headers=BaseData.headers
    )
    assert response.status_code == HTTPStatus.OK
    data = 'http://127.0.0.1:5000/auth/login?next=%2Fauth%2Frefresh'
    assert response.url == data


def test_logout(make_post_request):
    response = make_post_request('/auth/login', BaseData.login_data)
    assert response.status_code == HTTPStatus.OK

    logout = make_post_request('/auth/logout', BaseData.login_data)
    assert logout.status_code == HTTPStatus.OK


def test_logout_all(make_post_request):
    response = make_post_request('/auth/login', BaseData.login_data)
    assert response.status_code == HTTPStatus.OK

    logout = make_post_request('/auth/logout_all', BaseData.login_data)
    assert logout.status_code == HTTPStatus.OK
