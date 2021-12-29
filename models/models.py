from .dec_base import Base
from sqlalchemy import Column, Integer, String, DateTime
from controller.flask_controller import db
from datetime import datetime


class InstagramEntry(db.Model):

    __tablename__ = "InstagramInfo"

    id = Column(Integer, primary_key=True)
    follow_count = Column(Integer)
    followee_count = Column(Integer)
    date = Column(DateTime)
    num_posts = Column(Integer)
    total_likes = Column(Integer)
    total_comments = Column(Integer)

    def __init__(
        self,
        follow_count,
        followee_count,
        num_posts,
        total_likes,
        total_comments,
    ):
        self.follow_count = follow_count
        self.followee_count = followee_count
        self.date = datetime.now()
        self.num_posts = num_posts
        self.total_likes = total_likes
        self.total_comments = total_comments

    def __repr__(self):
        return f"Followers: {self.follow_count}, Following: {self.followee_count} (last checked on: {self.date})"


class SpotifyEntry(db.Model):

    __tablename__ = "SpotifyInfo"

    id = Column(Integer, primary_key=True)
    follow_count = Column(Integer)
    monthly_listeners = Column(Integer)
    date = Column(DateTime)

    def __init__(self, follow_count, monthly_listeners):
        self.follow_count = follow_count
        self.monthly_listeners = monthly_listeners
        self.date = datetime.now()

    def __repr__(self):
        return f"Followers: {self.follow_count}, Monthly listeners: {self.monthly_listeners} (last checked on: {self.date})"


class YoutubeEntry(db.Model):

    __tablename__ = "YoutubeInfo"

    id = Column(Integer, primary_key=True)
    sub_count = Column(Integer)
    total_views = Column(Integer)
    video_count = Column(Integer)
    date = Column(DateTime)

    def __init__(self, sub_count, total_views, video_count):
        self.sub_count = sub_count
        self.total_views = total_views
        self.video_count = video_count
        self.date = datetime.now()

    def __repr__(self):
        return f"Followers: {self.sub_count}, Total views: {self.total_views} (last checked on: {self.date})"
