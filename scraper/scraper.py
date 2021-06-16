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

    def initCredentials(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        with open(os.path.join(__location__, "credentials.json")) as creds:
            self.credentials = json.load(creds)
        self.instaloader = instaloader.Instaloader()

    def getInstagramStats(self):
        profile = instaloader.Profile.from_username(
            self.instaloader.context, "drowningempire"
        )

        return [profile.followers, profile.followees]

    def getSpotifyMonthlyListeners(self):
        url = "https://open.spotify.com/artist/34eXrgTr84KLThfaO8BAa8"
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")

        line = soup.find("meta", property="og:description")

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


# if __name__ == "__main__":
#     scraper = Scraper()
#     scraper.initCredentials()
#     scraper.getYouTubeStats()


# def other():
#     instaStats = scraper.getInstagramStats()
#     followers = instaStats[0]
#     followees = instaStats[1]
#     date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
#     insta = models.InstagramEntry(followers, followees, date_time)
#     print(insta)
#     scraper.getSpotifyFollowersWithAPI()
