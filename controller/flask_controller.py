from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from scraper.scraper import Scraper
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

from models.models import *


@app.route("/")
def home():
    scraper = Scraper()
    instaStats = scraper.getInstagramStats()
    followers = instaStats[0]
    followees = instaStats[1]
    date_time = datetime.now()
    insta = InstagramEntry(
        followCount=followers, followeeCount=followees, date=date_time
    )
    persistInstagramEntity(insta)
    return "<h1>Hello World</h1>"


def persistInstagramEntity(entity):
    db.session.add(entity)
    db.session.commit()
