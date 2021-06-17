import requests
import instaloader
import spotipy
import json, os
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from bs4 import BeautifulSoup
from googleapiclient.discovery import build


class Scraper:
    def __init__(self):
        self.credentials = {}
        self.instaloader = None
        self.instagramProfile = None

    def initCredentials(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        with open(os.path.join(__location__, "credentials.json")) as creds:
            self.credentials = json.load(creds)
        self.instaloader = instaloader.Instaloader(quiet=True)
        self.instaloader.load_session_from_file(
            self.credentials["instagram"]["user"]
        )

    def getInstagramStats(self):
        profile = instaloader.Profile.from_username(
            self.instaloader.context, "drowningempire"
        )
        self.instagramProfile = profile
        return [profile.followers, profile.followees]

    def getInstagramPostDetails(self):
        if self.instagramProfile is None:
            self.getInstagramStats()

        profile = self.instagramProfile
        post_array = []
        posts = list(profile.get_posts())
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

    def getSpotifyMonthlyListeners(self):
        url = "https://open.spotify.com/artist/34eXrgTr84KLThfaO8BAa8"
        page = requests.get(url, headers={"Cache-Control": "no-cache"})

        soup = BeautifulSoup(page.content, "html.parser")

        line = soup.find("meta", property="og:description")
        print(line)
        content = line["content"]
        content = content.split("Artist · ")[1]
        content = content.split(" monthly")[0]

        return content

    def getSpotifyFollowersWithAPI(self):
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

    def getSpotifyStats(self):
        followers = self.getSpotifyFollowersWithAPI()
        monthly_listeners = self.getSpotifyMonthlyListeners()
        return [followers, monthly_listeners]

    def getYouTubeStats(self):
        api_key = self.credentials["youtube"]["api_key"]

        youtube = build("youtube", "v3", developerKey=api_key)

        request = youtube.channels().list(
            part="statistics", id="UC8mxCHYWulqhfrgFC6cEq9Q"
        )

        response = request.execute()

        subCount = response["items"][0]["statistics"]["subscriberCount"]
        totalViewCount = response["items"][0]["statistics"]["viewCount"]

        with open("yt_response.json", "w") as jsonFile:
            json.dump(response, jsonFile, indent=4, sort_keys=False)

        return [subCount, totalViewCount]

    ## UTIL Methods ##

    def getMostLikedPost(self, posts):
        max = 0
        for post in posts:
            if max < post["likes"]:
                max = post["likes"]
        return max

    def getAvgLikes(self, posts):
        avg = 0
        total = 0
        for post in posts:
            total += post["likes"]
        avg = total / len(posts)
        return avg
