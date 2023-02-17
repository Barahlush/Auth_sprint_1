from peewee import CharField, Model


class Role(Model):
    name = CharField(unique=True)


def test_create_role(db):
    Role.create(name='test')
    db.commit()
    assert Role.get(name='test')


def test_delete_role(db):
    Role.create(name='test2')
    db.save()
    Role.delete().where(name='test2')
    assert Role.get(email='test@me.ru') is False


def test_get_roles(db):
    roles = Role.select().get()
    assert len(roles) > 0
