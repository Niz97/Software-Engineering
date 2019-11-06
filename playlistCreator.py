import os

import uuid
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

unqiueID = uuid.uuid4()
today = date.today()
date = today.strftime("%d/%m/%Y")

cid ="1d2c347f4e3d4b1e916066709832a6fa" 
secret = "c8a5fa505def47f984bf78021d91b5f5"
username = "x0pp22txvfpmd630upcjc573a"
SPOTIPY_REDIRECT_URL = 'http://localhost/'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope, cid, secret,SPOTIPY_REDIRECT_URL)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)


playlist_name = date+"-"+str(unqiueID)

#playlists = sp.user_playlist_create(username, playlist_name)
result = sp.search("track:brexit", type="track")
item = result['tracks']['items']
track = item[0]['artists']
trackID = track[0]['id']

print(trackID)
"""for item in result['tracks']['items']:
    track = item['artists']
    trackIDs = track[0]['id']"""


os.system("pause")