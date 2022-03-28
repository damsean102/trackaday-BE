import os
import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
from algoliasearch.search_client import SearchClient

load_dotenv()

# Algolia
ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")
ALGOLIA_API_KEY = os.getenv("ALGOLIA_API_KEY")
ALGOLIA_INDEX_NAME = os.getenv("ALGOLIA_INDEX_NAME")

# Spotify
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")
SPOTIFY_PLAYLIST_URI = os.getenv("SPOTIFY_PLAYLIST_URI")


sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_SECRET_ID))


client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
index = client.init_index(ALGOLIA_INDEX_NAME)



def url(value):
    if str(value).startswith('https://'):
        return str(value)
    else:
        return 'null';



offset = 0

# Create the empty list
tracks = [];

# Get teh Playlist details
response = sp.playlist(SPOTIFY_PLAYLIST_URI, fields='name, external_urls.spotify')

playlistName = response['name']
playlistURL = url(response['external_urls']['spotify'])

# Loop Through the Playlist tracks
while True:

    response = sp.playlist_tracks(SPOTIFY_PLAYLIST_URI, fields='items(track(id, name, duration_ms, artists.name, album.images, preview_url, external_urls.spotify), added_at),total', limit=100, offset=offset)

    # Loop Through Items
    for item in response['items']:
        itemTrack = item['track']

        artists = []
        for artist in itemTrack['artists']:
            artists.append(artist['name'])

        # Create the track in the format we want
        track = {
            'objectID': itemTrack['id'],
            'name': itemTrack['name'],
            'artists': artists,
            'duration': itemTrack['duration_ms'],
            'externalURL': url(itemTrack['external_urls']['spotify']),
            'previewUrl': url(itemTrack['preview_url']),
            'thumbnailURL': url(itemTrack['album']['images'][0]['url']),
            'addedAt': item['added_at'],
            'playlistName': playlistName,
            'playlistUrl': playlistURL,
        }
        tracks.append(track)

    offset = offset + len(response['items'])

    # print(offset, "/", response['total'])
    # print(response['items'])


    if len(response['items']) == 0:
        break

# Repint out the Tracks object
# pprint(tracks)

# Push to Algolia
res = index.save_objects(tracks, {
    'autoGenerateObjectIDIfNotExist': False
}).wait()
