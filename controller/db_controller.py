from .flask_controller import db


def persistInstagramEntity(entity):
    db.session.add(entity)
