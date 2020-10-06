import os
import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")
PLAYLIST_URI = os.getenv("SPOTIFY_PLAYLIST_ID")

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=SECRET_ID))

offset = 0

while True:
    response = sp.playlist_tracks(PLAYLIST_URI, fields='items(track(name, artists.name, external_urls.spotify)),total', limit=100, offset=offset)
    pprint(response['items'])
    offset = offset + len(response['items'])
    print(offset, "/", response['total'])

    if len(response['items']) == 0:
        break
