from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from scraper.scraper import Scraper
from datetime import datetime


app = Flask(__name__, template_folder="../templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

from models.models import *
from . import db_controller

scraper = Scraper()


@app.route("/")
def home():

    scraper.initCredentials()
    instaStats = scraper.getInstagramStats()
    followers = instaStats[0]
    followees = instaStats[1]
    date_time = datetime.now()
    insta = InstagramEntry(
        followCount=followers, followeeCount=followees, date=date_time
    )

    yt_stats = scraper.getYouTubeStats()

    spotify_stats = scraper.getSpotifyStats()

    return render_template(
        "index.html",
        subcount=yt_stats[0],
        totalViews=yt_stats[1],
        instaFollowers=followers,
        instaFollowees=followees,
        spotifyFollowers=spotify_stats[0],
        spotifyMonthly=spotify_stats[1],
    )
