import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import sys

# Globals
CLIENT_ID = '57a43e229eb045f7902cfb5a723d0e59'
CLIENT_SECRET = 'f301225d3cc3449ba674a36ee64a1cbf'

# Spotify Object
sp = None

class WrapperClass:
    def __init__(self):
        self.CLIENT_ID = '57a43e229eb045f7902cfb5a723d0e59'
        self.CLIENT_SECRET = 'f301225d3cc3449ba674a36ee64a1cbf'

        self.sp = self.doAuth()

    def doAuth(self):
        '''
            Funtion: Setup and initialization of credentials manager and 
            master Spotify object

            Returns: Spotify Object
        '''

        credentialsManager = \
        SpotifyClientCredentials(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET)
        
        sp = spotipy.Spotify(client_credentials_manager=credentialsManager)
        return sp 

    def getUsersPlaylists(self, username='mikeydays'):  
        '''
            Function: Get a list of users playlist names

            Returns: A list of names
        '''
        playlistNames = []
        playlistUris = []
        playlists = self.sp.user_playlists(username)

        for p in playlists['items']:
            playlistNames.append(p['name'].encode('ascii', 'ignore').decode('ascii'))
            playlistUris.append(p['uri'].split(':')[2])

        
        return pd.DataFrame({'name' : playlistNames, 'uri' : playlistUris}, \
         columns=['name', 'uri'])

    def getName(self, results, nameArr):
            tl = []
            for i, item in enumerate(results['items']):
                
                track = item['track']
                name = track['name']
                uri = track['uri']

                artistName = track['artists'][0]['name']

                result = self.sp.search(artistName)
                track = result['tracks']['items'][0]
                artist = self.sp.artist(track["artists"][0]["external_urls"]["spotify"])
                genres = artist["genres"]
               

                tl.append((name, uri.split(':')[2], genres))

            return tl
    
    def getSongsFromPlaylist(self, uri, username, name=""):
        ''' 
            Function: Get list of songs from certain playlist

            Returns: Dataframe containing [song name, uri]
        '''

        trackList = []
        results = self.sp.user_playlist(username, uri)
        tracks = results['tracks']
       
        trackList.extend(self.getName(tracks, trackList))
        while(tracks['next']):
            tracks = self.sp.next(tracks)
           
            trackList.extend(self.getName(tracks, trackList))

        names = [tuple[0] for tuple in trackList]
        uris = [tuple[1] for tuple in trackList]
        genres = [tuple[2] for tuple in trackList]

        return pd.DataFrame(data={'name' : names, 'uri' : uris, 'genres': genres})  

    
    def getPlaylistGenre(self, songsDF):
        genreCounter = {}
        for genres in songsDF['genres']:
            for genre in genres:
                if genreCounter.get(genre) == None:
                    genreCounter[genre] = 1
                else:
                    genreCounter[genre] += 1
        return genreCounter


    def find_genre(self, names):
        count = 0
        name = names.tolist()
        final = []
        for i in names:
            genres = []
            if i ==[]:
                final.append("")
                continue
            for word in i:
                words = word.split()
                for j in words:
                    genres.append(j)
            final.append(pd.Series(genres).value_counts().sort_values(ascending=False).index.tolist()[0])
        return final

print('Running')


# w = WrapperClass()
# w.doAuth()
# w.getUsersPlaylists('mikeydays')
# print(w.getSongsFromPlaylist('0ZB9jG1uyCbs4rnQ1V5ro6', 'mikeydays'))

# lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'


# results = sp.artist_top_tracks(lz_uri)

# for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()



