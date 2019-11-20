'''
@Description: Create a Spotify playlist.
@Version: 2.2.0.20191118
@Author: William Staff (driver) and Jichen Zhao(observer)
@Date: 2019-11-06 23:55:01
@Last Editors: Jichen Zhao
@LastEditTime: 2019-11-20 15:30:02
'''

import os

from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from logTool import Log

def createPlaylist(token, newsSource, keywords):

	time = datetime.today()
	newsDate = time.strftime('%H:%M-%d/%m/%Y')
	trackIDs = []

	if token:
		sp = spotipy.Spotify(auth = token)
		username = sp.current_user()['id']
		playlist_name = newsSource + '-' + newsDate
		playlists = sp.user_playlist_create(username, playlist_name)
		
		for termArray in keywords:
			for term in termArray:
				result = sp.search('track:'+term, type='track', limit = 1)
				item = result['tracks']['items']
				
				if len(item) > 0:
					trackIDs.append(item[0]['uri'])
		for i in range(0,70):
			trackIDs.append(trackIDs[0])
		if len(trackIDs) == 0:
			Log('warning', 'The playlist is empty.')
		else:
			if len(trackIDs) > 100:
				sp.user_playlist_add_tracks(username, playlists['id'], [trackIDs[count] for count in range(100)])
				sp.user_playlist_add_tracks(username, playlists['id'], [trackIDs[count] for count in range(100, len(trackIDs))])
			else:
				sp.user_playlist_add_tracks(username, playlists['id'], trackIDs)
		
		return playlists['external_urls']['spotify']
	else:
		Log('warning', 'Cannot get Spotify access token.')
		return ''