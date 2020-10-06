from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint

import os

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=SECRET_ID))

pl_id = 'spotify:playlist:5RmD55dvRIE5AdhzdYwi4b'
offset = 0

while True:
    response = sp.playlist_tracks(pl_id, fields='items(track.name,track.artists.name),total', limit=100, offset=offset)
    pprint(response['items'])
    offset = offset + len(response['items'])
    print(offset, "/", response['total'])

    if len(response['items']) == 0:
        break
