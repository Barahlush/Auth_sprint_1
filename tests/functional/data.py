users = [
    {
        'id': '73n20a54-b794-41c3-84c1-ac6347204b14',
        'email': 'tatsu@ya.ru',
        'password': 'test_user',
        'fs_uniquifier': 'text',
    },
    {
        'id': '5f5b4820-1788-488b-916b-285708fb2d1d',
        'email': 'admin@ya.ru',
        'password': 'test_moderator',
        'fs_uniquifier': 'text2',
    },
    {
        'id': 'b236e851-90b0-4fda-a86e-32c331f5ae73',
        'email': 'admin@ya.ru',
        'password': 'test_admin',
        'fs_uniquifier': 'text3',
    },
]

roles = [
    {
        'id': 'cb8d7e85-3452-4399-b05f-0be43382666e',
        'name': 'monitor',
        'permissions': {'admin-read', 'user-read'},
    },
    {
        'id': '477e6882-afea-4d09-a6bd-4aba0eb34d90',
        'name': 'user',
        'permissions': {'user-read', 'user-write'},
    },
    {
        'id': '488e76ed-642a-4c65-9589-ba547551dd26',
        'name': 'admin',
        'permissions': {
            'admin-read',
            'admin-write',
            'user-read',
            'user-write',
        },
    },
]
