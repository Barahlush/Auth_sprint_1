from functional.settings import TestSettings

settings = TestSettings()


class BaseData:
    name = 'test'
    email = 'test@mail.ru'
    password = 'test'
    fs_uniquifier = 'fgkhfdsfgk_fghg_hghgjghjghklj_kjl'
    active = True
    signup_data = {
        'name': name,
        'email': email,
        'password': password,
        'fs_uniquifier': fs_uniquifier,
        'active': active,
    }
    login_data = {
        'email': email,
        'password': password,
        'fs_uniquifier': fs_uniquifier,
        'active': active,
    }
    invalid_login_data = {
        'email': email,
        'password': 'invalid',
        'fs_uniquifier': fs_uniquifier,
        'active': active,
    }


def test_sign_up(make_post_request):
    response = make_post_request('/auth/register', data=BaseData.signup_data)
    assert response.status_code == 201 or 202


def test_success_login(make_post_request):
    response = make_post_request('/auth/login', BaseData.login_data)
    assert response.status_code == 201
    data = response.json()
    assert data[0].get('access_token') is not None
    assert data[1].get('refresh_token') is not None


def test_failed_login(make_post_request):
    response = make_post_request('/auth/login', BaseData.invalid_login_data)
    assert response.status_code == 403


def test_change_password(make_post_request):
    response = make_post_request('/auth/login', BaseData.login_data)
    assert response.status_code == 201

    data = response.json()
    access_token = data[0]
    assert access_token is not None

    email = BaseData.email
    old_password = BaseData.password
    password = 'change'
    change_data = {
        'email': email,
        'old_password': old_password,
        'new_password': password,
    }
    change = make_post_request(
        '/auth/change_password', data=change_data, headers=access_token
    )
    assert change.status_code == 200

    response = make_post_request(
        '/auth/login', {'email': email, 'password': password}
    )
    assert response.status_code == 201

    return_old_password = {
        'email': email,
        'old_password': password,
        'new_password': old_password,
    }
    change = make_post_request(
        '/auth/change_password', data=return_old_password, headers=access_token
    )
    assert change.status_code == 200
