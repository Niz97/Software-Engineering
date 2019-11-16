import os

import uuid
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from logTool import Log

def createPlaylist(keywords):

	unqiueID = uuid.uuid4()
	today = date.today()
	newsDate = today.strftime("%d/%m/%Y")
	trackIDs = []

	cid ="b80c9d43d197499f8df5e1e438331a3a" 
	secret = "82ed92de9f1a450a85115d342ca696e2"
	username = "uu8bhrprx5sfo9oasyf36hbxz"
	SPOTIPY_REDIRECT_URL = 'http://localhost/'

	client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	scope = 'playlist-modify-public'
	token = util.prompt_for_user_token(username, scope, cid, secret,SPOTIPY_REDIRECT_URL)

	if token:
	    sp = spotipy.Spotify(auth=token)
	else:
	    Log('warning', "Can't get token for" + username)


	playlist_name = newsDate+"-"+str(unqiueID)
	playlists = sp.user_playlist_create(username, playlist_name)


	for termArray in keywords:
		for term in termArray:
			try:
				result = sp.search("track:"+term, type="track")
				item = result['tracks']['items']
				trackIDs.append(item[0]['uri'])
			except Exception as e:
				Log('error', repr(e))


	playlists = sp.user_playlists(username)
	for playlist in playlists['items']:
	    if playlist['owner']['id'] == username:
	        if playlist['name'] == playlist_name:
	            for i in range(len(trackIDs)):
	                sp.user_playlist_add_tracks(username, playlist['id'], trackIDs)


# test purposes only
if __name__ == '__main__':
    from pullNews import get_headlines
    from keywordExtractor import ExtractKeywords

    urlList = get_headlines('gb')
    keywordList = ExtractKeywords(urlList)
    createPlaylist(keywordList) # TODO: what if the keyword list is empty?