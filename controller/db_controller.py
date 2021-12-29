from models.models import InstagramEntry, SpotifyEntry, YoutubeEntry
from .flask_controller import db


def init_db():
    return True


def persist_entity(entity):
    try:
        db.session.add(entity)
        db.session.commit()
    except:
        db.session.rollback()


def persist_entities(entities: list):
    try:
        for entity in entities:
            db.session.add(entity)
        db.session.commit()
    except:
        db.session.rollback()


def get_all_entries(entityType):
    if entityType is "Instagram":
        return InstagramEntry.query.all()
    elif entityType is "Spotify":
        return SpotifyEntry.query.all()
    elif entityType is "YouTube":
        return YoutubeEntry.query.all()
    else:
        return []


def delete_entry(entity):
    db.session.delete(entity)
    db.session.commit()


def delete_all_entries(entityType):
    try:
        if entityType is "Instagram":
            num_deleted = InstagramEntry.query.delete()
            db.session.commit()
            return num_deleted
        elif entityType is "Spotify":
            num_deleted = SpotifyEntry.query.delete()
            db.session.commit()
            return num_deleted
        elif entityType is "YouTube":
            num_deleted = YoutubeEntry.query.delete()
            db.session.commit()
            return num_deleted
        else:
            return 0
    except:
        db.session.rollback()
