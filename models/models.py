from .dec_base import Base
from sqlalchemy import Column, Integer, String, DateTime
from controller.flask_controller import db


class InstagramEntry(db.Model):

    __tablename__ = "InstagramInfo"

    id = Column(Integer, primary_key=True)
    followCount = Column(Integer)
    followeeCount = Column(Integer)
    date = Column(DateTime)

    def __init__(self, followCount, followeeCount, date):
        self.followCount = followCount
        self.followeeCount = followeeCount
        self.date = date

    def __repr__(self):
        return f"Followers: {self.followCount}, Following: {self.followeeCount} (last checked on: {self.date})"


class SpotifyEntry(db.Model):

    __tablename__ = "SpotifyInfo"

    id = Column(Integer, primary_key=True)
    followCount = Column(Integer)
    monthly_listeners = Column(Integer)
    date = Column(DateTime)

    def __init__(self, followCount, monthly_listeners, date):
        self.followCount = followCount
        self.monthly_listeners = monthly_listeners
        self.date = date

    def __repr__(self):
        return f"Followers: {self.followCount}, Monthly listeners: {self.monthly_listeners} (last checked on: {self.date})"


class YoutubeEntry(db.Model):

    __tablename__ = "YoutubeInfo"

    id = Column(Integer, primary_key=True)
    subCount = Column(Integer)
    totalViews = Column(Integer)
    date = Column(DateTime)

    def __init__(self, subCount, totalViews, date):
        self.subCount = subCount
        self.totalViews = totalViews
        self.date = date

    def __repr__(self):
        return f"Followers: {self.subCount}, Total views: {self.totalViews} (last checked on: {self.date})"
