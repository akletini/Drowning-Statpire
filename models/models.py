from .dec_base import Base
from sqlalchemy import Column, Integer, String, Date


class InstagramEntry(Base):

    __tablename__ = "instagramPosts"

    id = Column(Integer, primary_key=True)
    followCount = Column(Integer)
    followeeCount = Column(Integer)
    date = Column(Date)

    def __init__(self, followCount, followeeCount, date):
        self.followCount = followCount
        self.followeeCount = followeeCount
        self.date = date

    def __repr__(self):
        return f"Followers: {self.followCount}, Following: {self.followeeCount} (last checked on: {self.date})"
