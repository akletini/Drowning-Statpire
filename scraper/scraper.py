import requests
import instaloader
import spotipy
import json, os, re
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from bs4 import BeautifulSoup
from googleapiclient.discovery import build


class Scraper:
    def __init__(self):
        self.credentials = {}
        self.instaloader = None
        self.instagramProfile = None
        self.instagramPosts = None

    def init_credentials(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        with open(os.path.join(__location__, "credentials.json")) as creds:
            self.credentials = json.load(creds)
        self.instaloader = instaloader.Instaloader(quiet=True)
        self.instaloader.load_session_from_file(
            self.credentials["instagram"]["user"]
        )

    def get_instagram_stats(self):
        profile = instaloader.Profile.from_username(
            self.instaloader.context, "drowningempire"
        )
        self.instagramProfile = profile
        return [
            profile.followers,
            profile.followees,
            list(profile.get_posts()),
        ]

    def get_instagram_post_details(self):
        if self.instagramProfile is None:
            self.get_instagram_stats()

        profile = self.instagramProfile
        post_array = []
        posts = list(profile.get_posts())
        self.instagramPosts = posts
        post_count = len(posts)
        i = 0
        for post in posts:
            id = post_count - i
            comment_count = post.comments
            like_count = post.likes
            post_date = post.date.strftime("%d.%m.%Y at %H:%M:%S")
            post_array.append(
                {
                    "id": id,
                    "likes": like_count,
                    "comments": comment_count,
                    "date": post_date,
                }
            )
            i += 1
        return post_array

    def get_spotify_monthly_listeners(self):
        url = "https://open.spotify.com/artist/34eXrgTr84KLThfaO8BAa8"
        session = requests.session()
        page = session.get(
            url, headers={"Cache-Control": "max-age=3000, must-revalidate", "User-Agent": "Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187 Safari/537.36"}
        )
        session.cookies.clear()
        soup = BeautifulSoup(page.content, "html.parser")

        line = soup.find("meta", property="og:description")
        print(line)

        content = -1
        try:
            content = line["content"]
            content = content.split("Artist · ")[1]
            content = content.split(" monthly")[0]
        except:
            pass
        

        return content

    def get_spotify_followers_with_API(self):
        client_id = self.credentials["spotify"]["client_id"]
        client_secret = self.credentials["spotify"]["client_secret"]

        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )

        artist_id = "spotify:artist:34eXrgTr84KLThfaO8BAa8"
        artist = sp.artist(artist_id)

        followers = artist["followers"]["total"]
        return followers

    def get_spotify_stats(self):
        followers = self.get_spotify_followers_with_API()
        monthly_listeners = self.get_spotify_monthly_listeners()
        return [followers, monthly_listeners]

    def get_youtube_stats(self):
        api_key = self.credentials["youtube"]["api_key"]

        youtube = build("youtube", "v3", developerKey=api_key)

        request = youtube.channels().list(
            part="statistics", id="UC8mxCHYWulqhfrgFC6cEq9Q"
        )

        response = request.execute()

        sub_count = response["items"][0]["statistics"]["subscriberCount"]
        total_view_count = response["items"][0]["statistics"]["viewCount"]
        video_count = response["items"][0]["statistics"]["videoCount"]

        with open("yt_response.json", "w") as jsonFile:
            json.dump(response, jsonFile, indent=4, sort_keys=False)

        return [sub_count, total_view_count, video_count]

    ## UTIL Methods ##

    def get_most_likes_on_post(self, posts):
        max = 0
        for post in posts:
            if max < post["likes"]:
                max = post["likes"]
        return max

    def get_most_comments_on_post(self, posts):
        max = 0
        for post in posts:
            if max < post["comments"]:
                max = post["comments"]
        return max

    def get_avg_likes(self, posts):
        avg = 0
        total = 0
        for post in posts:
            total += post["likes"]
        avg = total / len(posts)
        return avg

    def get_avg_comments(self, posts):
        avg = 0
        total = 0
        for post in posts:
            total += post["comments"]
        avg = total / len(posts)
        return avg
