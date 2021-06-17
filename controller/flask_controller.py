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
scraper.initCredentials()

crawled_info = []
instagram_posts = []


@app.route("/")
def home():
    global crawled_info
    if not crawled_info:
        insta_stats = scraper.getInstagramStats()
        yt_stats = scraper.getYouTubeStats()
        spotify_stats = scraper.getSpotifyStats()
        crawled_info = [insta_stats, yt_stats, spotify_stats]

    insta_stats = crawled_info[0]
    yt_stats = crawled_info[1]
    spotify_stats = crawled_info[2]

    return render_template(
        "index.html",
        subcount=yt_stats[0],
        totalViews=yt_stats[1],
        instaFollowers=insta_stats[0],
        instaFollowees=insta_stats[1],
        spotifyFollowers=spotify_stats[0],
        spotifyMonthly=spotify_stats[1],
    )


@app.route("/instagramDetails")
def instaDetails():
    global instagram_posts
    if not instagram_posts:
        instagram_posts = scraper.getInstagramPostDetails()
    avg = scraper.getAvgLikes(instagram_posts)
    print(avg)
    return render_template("instagramDetails.html", post_array=instagram_posts)


@app.route("/spotifyDetails")
def spotifyDetails():
    return render_template("spotifyDetails.html")


@app.route("/youtubeDetails")
def youtubeDetails():
    return render_template("youtubeDetails.html")


@app.route("/update")
def update():
    global crawled_info
    crawled_info = []
    return redirect("/")
