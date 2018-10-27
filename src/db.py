import models

db = models.db


def get_user(user):
    u = models.User.query.filter_by(name=user).first()
    db.session.commit()
    return u


def get_proxy(user):
    return get_user(user).proxy


def add_user(name, proxy, instance):
    db.session.add(models.User(name=name, proxy=proxy, instance=instance))
    db.session.commit()


def delete(user):
    models.User.query.filter_by(name=user).delete()
    db.session.commit()
