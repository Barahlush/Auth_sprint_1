from peewee import BooleanField, Model, TextField


class User(Model):
    email = TextField()
    password = TextField()
    fs_uniquifier = TextField(null=False)
    active = BooleanField(default=True)


def test_create_user(db):
    User.create(
        email='test@me.ru',
        password='password',
        fs_uniquifier='text',
        roles=['admin'],
    )
    db.commit()
    assert User.get(email='test@me.ru')


def test_delete_user(db):
    User.create(
        email='test@me.ru',
        password='password',
        fs_uniquifier='text',
        roles=['admin'],
    )
    db.save()
    User.delete().where(email='test@me.ru')
    assert User.get(email='test@me.ru') is False


def test_get_users(db):
    roles = User.select().get()
    assert len(roles) > 0
