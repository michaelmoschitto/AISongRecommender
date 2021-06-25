import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import sys
from datetime import timedelta
from spotipy.oauth2 import SpotifyOAuth
import json

# Globals
# CLIENT_ID = '57a43e229eb045f7902cfb5a723d0e59'
# CLIENT_SECRET = 'f301225d3cc3449ba674a36ee64a1cbf'
# ------Michael's ^^------

CLIENT_ID = 'dc047bd4521147558724b09377f6ea08'
CLIENT_SECRET = 'd5b1793f01504e61ba3effe63af5b89f'
# Spotify Object
sp = None

# +
class WrapperClass:
    def __init__(self):
        # self.CLIENT_ID = '57a43e229eb045f7902cfb5a723d0e59'
        # self.CLIENT_SECRET = 'f301225d3cc3449ba674a36ee64a1cbf'
        # ------Michael's ^^------

        self.CLIENT_ID = 'dc047bd4521147558724b09377f6ea08'
        self.CLIENT_SECRET = 'd5b1793f01504e61ba3effe63af5b89f'


        self.sp = self.doAuth()

    def doAuth(self, scope="playlist-modify-public"):
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

    def getName(self, results, nameArr, sp):
            tl = []
            for i, item in enumerate(results['items']):
                
                track = item['track']
                name = track['name']
                uri = track['uri']
                artistName = track['artists'][0]['name']

                result = sp.search(artistName)
                track = result['tracks']['items'][0]
                artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
                genres = artist["genres"]
               

                tl.append((name, uri.split(':')[2], genres, artistName))

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
        artists = [tuple[3] for tuple in trackList]

        return pd.DataFrame(data={'name' : names, 'uri' : uris, 'genres': genres, 'artist' : artists}) 

    def getMySavedSongs(self):
        ''' 
            Function: Get all of current users saved (liked) songs

            Returns: Dataframe containing [song name, uri]
        '''
        token = 'BQBwpaZkZ5h2NuAlgepObTSrEJPHVgV9YffJsNZZgQ0wPKgFoJ12RCrsboFtINQEd6ywXK050P4gUbQ_77GiM5ZTVn_G1_3YroZUgWWht87B4Qg_QOmcYdi-8gOhaz0HEdrxpnO952WLUTaW-sfiQgOu5K8ME3LChkwWihuLNzSZoEHr1vw7VPhnvl7eqTmgvkM'
        sp = spotipy.Spotify(auth=token)

        trackList = []
        tracks = sp.current_user_saved_tracks()
        items = tracks['items']

        with open('NateOut.txt', 'w') as outfile:
            json.dump(items[0], outfile)
        # print(items)
        # return 
        trackList.extend(self.getName(tracks, trackList, sp))
        while(tracks['next']):
            tracks = sp.next(tracks)

            trackList.extend(self.getName(tracks, trackList, sp))

        names = [tuple[0] for tuple in trackList]
        uris = [tuple[1] for tuple in trackList]
        genres = [tuple[2] for tuple in trackList]
        artists = [tuple[3] for tuple in trackList]

        return pd.DataFrame(data={'name': names, 'uri': uris, 'genres': genres, 'artist': artists})

    
    def getPlaylistGenre(self, songsDF):
        genreCounter = {}
        for genres in songsDF['genres']:
            for genre in genres:
                if genreCounter.get(genre) == None:
                    genreCounter[genre] = 1
                else:
                    genreCounter[genre] += 1
        return genreCounter


    def findGenre(self, names):
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

    def getFeatures(self, songsDF):
        names = []


        featureList = []
        acousticness = []
        danceability = []
        energy = []
        instrumentalness = []
        liveness = []
        loudness = []
        speechiness = []
        tempo = []
        valence = []
        popularity = []
        timeSignature = []
        length = []

        for index, row in songsDF.iterrows():
            uri = row['uri']
            if(not isinstance(uri, str)):
                continue
            name = row['name']
            features = self.sp.audio_features(uri)
            if features != [None]:
                names.append(name)
                length.append(
                    timedelta(milliseconds=features[0]['duration_ms']))
                acousticness.append(features[0]['acousticness'])
                danceability.append(features[0]['danceability'])
                energy.append(features[0]['energy'])
                instrumentalness.append(features[0]['instrumentalness'])
                liveness.append(features[0]['liveness'])
                loudness.append(features[0]['loudness'])
                speechiness.append(features[0]['speechiness'])
                tempo.append(features[0]['tempo'])
                valence.append(features[0]['valence'])
                timeSignature.append(features[0]['time_signature'])

                # popularity.append(features[0]['popularity'])

        data = {
            'name': names,
            'length': length,
            'acousticness': acousticness,
            'danceability': danceability,
            'energy': energy,
            'instrumentalness': instrumentalness,
            'liveness': liveness,
            'loudness': loudness,
            'speechiness': speechiness,
            'tempo': tempo,
            'valence': valence,
            'timeSignature': timeSignature
        }

        return pd.DataFrame(data)
    
    def createPlaylist(self, userId=None, name='testPlaylist', trackIdList=None):
        if userId == None or trackIdList == None:
            print('userId and track Ids cannot be None')
            return
        
        scope = "playlist-modify-public"
        token = 'BQAl3KYPddHApFUF6JCSoGNNTwWMXsBO3b-oDPj3D6wYseqhwcfmcc3uqpwq41zAMTu22OI4k31wcHFVia9NoJ_DIVo-SblDi1ywAjnhYqpNxcsBzMxhV5GX8nPomdkn0p1AJtsO3mlP8G-pLiTqQWhgRjiXgLOlhrLLJShQtGDXDKF-EYvk3Akn3VHEHaTMoBE'
        sp = spotipy.Spotify(auth=token)
        # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=scope, redirect_uri='localhost:3000/callback'))
        user_id = sp.me()['id']
        print(user_id)
        
        output = sp.user_playlist_create(user_id, name, public=True)
        playlistId = output['id']

        sp.user_playlist_add_tracks(user_id, playlistId, trackIdList[:99])
        sp.user_playlist_add_tracks(user_id, playlistId, trackIdList[99:188])
        sp.user_playlist_add_tracks(user_id, playlistId, trackIdList[188:287])
        sp.user_playlist_add_tracks(user_id, playlistId, trackIdList[287:386])
        sp.user_playlist_add_tracks(user_id, playlistId, trackIdList[386:485])
        sp.user_playlist_add_tracks(user_id, playlistId, trackIdList[485:584])
        sp.user_playlist_add_tracks(user_id, playlistId, trackIdList[584:684])
        sp.user_playlist_add_tracks(user_id, playlistId, trackIdList[684:783])
        sp.user_playlist_add_tracks(user_id, playlistId, trackIdList[783:882])
        sp.user_playlist_add_tracks(user_id, playlistId, trackIdList[882:])









        
# -

# print('Running')


# w = WrapperClass()

# songsDF = pd.read_csv('./Data/mikeydays/country/SongDF.csv')
# print(w.getFeatures(songsDF))
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

# -------------Write Songs to Spotify-------------
# w = WrapperClass()
# w.doAuth()
# energeticTrackIds = list(pd.read_csv('./Data/mikeydays/Calm.csv')['uri'].values)
# # print(energeticTrackIds)
# w.createPlaylist('mikeydays', 'PetesCalmSongs', energeticTrackIds)
# -----------------------------------------------------------------


# w = WrapperClass()
# # w.doAuth()
# outDF = w.getMySavedSongs()
# outDF.to_csv('NatesDF.csv', index=False)




# tracks = results['tracks']

# print(results)
# # print(access_token)

w = WrapperClass()
w.doAuth()
URIs = list(pd.read_csv('./NateData/EverythingElse.csv')['uri'].values)
print(URIs)
print(len(URIs))
# print(energeticTrackIds)
w.createPlaylist('natefay', 'Errythang Else', URIs)
