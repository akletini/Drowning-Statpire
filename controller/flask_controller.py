from re import sub
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from scraper.scraper import Scraper
from datetime import datetime
import os, shutil, time, threading, schedule


app = Flask(
    __name__, template_folder="../templates", static_folder="../static"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../site.db"
db = SQLAlchemy(app)

from models.models import *
from . import db_controller

scraper = Scraper()
scraper.init_credentials()

crawled_info = []
instagram_posts = []
first_execution = True


@app.route("/")
def home():
    global crawled_info
    global first_execution
    if not crawled_info:
        insta_stats = scraper.get_instagram_stats()
        yt_stats = scraper.get_youtube_stats()
        spotify_stats = scraper.get_spotify_stats()
        crawled_info = [insta_stats, yt_stats, spotify_stats]

    insta_stats = crawled_info[0]
    yt_stats = crawled_info[1]
    spotify_stats = crawled_info[2]

    if first_execution:
        db.create_all()
        schedule.every().day.at("08:00").do(write_stats_to_db)
        schedule.every().day.at("20:00").do(write_stats_to_db)
        thread = run_continuously()
        first_execution = False

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
def instagram_details():
    global crawled_info
    global instagram_posts
    if not instagram_posts:
        instagram_posts = scraper.get_instagram_post_details()

    insta_stats = crawled_info[0]
    avg_likes = "{:10.1f}".format(scraper.get_avg_likes(instagram_posts))
    avg_comments = "{:10.1f}".format(scraper.get_avg_comments(instagram_posts))
    max_likes = scraper.get_most_likes_on_post(instagram_posts)
    max_comments = scraper.get_most_comments_on_post(instagram_posts)

    return render_template(
        "instagramDetails.html",
        followers=insta_stats[0],
        avgLikes=avg_likes,
        avgComments=avg_comments,
        maxLikes=max_likes,
        maxComments=max_comments,
    )


@app.route("/instagramDetails/allPosts")
def insta_all_posts():
    global instagram_posts
    if not instagram_posts:
        instagram_posts = scraper.get_instagram_post_details()
    avg = scraper.get_avg_likes(instagram_posts)
    return render_template("instagramPosts.html", post_array=instagram_posts)


@app.route("/spotifyDetails")
def spotify_details():
    return render_template("spotifyDetails.html")


@app.route("/youtubeDetails")
def youtube_details():
    return render_template("youtubeDetails.html")


@app.route("/update")
def update():
    global crawled_info
    crawled_info = []
    return redirect("/")


@app.route("/instagramDetails/allPosts/<id>")
def dl_last(id):
    global instagram_posts, scraper
    posts = scraper.instagramPosts
    current_post = posts[int(id)]
    caption = current_post.caption
    hashtags = current_post.caption_hashtags
    comments = current_post.get_comments()

    ## set image folder and empty it if files exist
    folder = os.path.join(os.getcwd(), "static")
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))

    ## get image
    image_location = "static"
    scraper.instaloader.download_post(
        current_post,
        image_location,
    )
    files = os.listdir(image_location)
    image_path = None
    for file in files:
        if file.endswith(".jpg"):
            image_path = file

    return render_template(
        "instagramPostView.html", caption=caption, imagePath=image_path
    )


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def write_stats_to_db():
    print(
        f"Written to database at {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
    )
    insta_stats = scraper.get_instagram_stats()
    yt_stats = scraper.get_youtube_stats()
    spotify_stats = scraper.get_spotify_stats()

    # Instagram prep
    posts = insta_stats[2]
    num_posts = len(posts)
    total_likes = 0
    total_comments = 0
    for post in posts:
        total_likes += post.likes
        total_comments += post.comments

    instagram_entry = InstagramEntry(
        follow_count=insta_stats[0],
        followee_count=insta_stats[1],
        num_posts=num_posts,
        total_likes=total_likes,
        total_comments=total_comments,
    )

    # YouTube prep
    youtube_entry = YoutubeEntry(
        sub_count=yt_stats[0], total_views=yt_stats[1], video_count=yt_stats[2]
    )

    # Spotify prep
    spotify_entry = SpotifyEntry(
        follow_count=spotify_stats[0], monthly_listeners=spotify_stats[1]
    )
    with app.app_context():
        db_controller.persist_entities(
            [instagram_entry, youtube_entry, spotify_entry]
        )

    os.system("python3 write_db_to_drive.py")
    return render_template(
        "index.html",
        subcount=yt_stats[0],
        totalViews=yt_stats[1],
        instaFollowers=insta_stats[0],
        instaFollowees=insta_stats[1],
        spotifyFollowers=spotify_stats[0],
        spotifyMonthly=spotify_stats[1],
    )
