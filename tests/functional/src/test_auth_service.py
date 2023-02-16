from functional.settings import TestSettings

settings = TestSettings()


class BaseData:
    name = 'test'
    email = 'test@mail.ru'
    password = 'test'
    fs_uniquifier = 'test'
    signup_data = {
        'name': name,
        'email': email,
        'password': password,
        'fs_uniquifier': fs_uniquifier,
    }
    login_data = {'email': email, 'password': password}
    invalid_login_data = {'email': email, 'password': 'invalid'}


def test_sign_up(make_post_request):
    response = make_post_request('/register', data=BaseData.signup_data)
    assert response.status_code == 201 or 202


# def test_success_login(make_post_request):
#     response = make_post_request('/login', BaseData.login_data)
#     assert response.status_code == 201
#     data = response.json()
#     assert data[0].get('access_token') is not None
#     assert data[1].get('refresh_token') is not None


# def test_failed_login(make_post_request):
#     """Тест на ввод неверных данных в login"""
#     response = make_post_request('/login', BaseData.invalid_login_data)
#     assert response.status_code == 403


# def test_refresh(make_post_request):
#     """Тест на login юзера и обмен его refresh_token
#     на новую пару refresh+access"""


# def test_check_history(make_get_request, make_post_request):


# def test_change_password(make_post_request):
#     """Тест на изменение пароля:
#     Залогиниться -> получить токен -> изменить пароль ->
#     залогиниться еще раз -> вернуть все обратно"""
#
#     assert access_token is not None


# def test_change_personal_data(make_post_request):
#     """Тест на изменение name и email:
#     Залогиниться -> получить токен -> поменять данные ->
#     залогиниться еще раз -> вернуть все обратно"""
#
#     assert access_token is not None
#
#         'new_name': new_name}
