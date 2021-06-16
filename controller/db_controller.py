from models.models import InstagramEntry, SpotifyEntry, YoutubeEntry
from .flask_controller import db


def persistEntity(entity):
    try:
        db.session.add(entity)
        db.session.commit()
    except:
        db.session.rollback()


def getAllEntries(entityType):
    if entityType is "Instagram":
        return InstagramEntry.query.all()
    elif entityType is "Spotify":
        return SpotifyEntry.query.all()
    elif entityType is "YouTube":
        return YoutubeEntry.query.all()
    else:
        return []


def deleteEntry(entity):
    db.session.delete(entity)
    db.session.commit()


def deleteAllEntries(entityType):
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
