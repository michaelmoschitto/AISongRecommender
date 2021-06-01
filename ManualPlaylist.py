import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import sys
from datetime import timedelta
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '57a43e229eb045f7902cfb5a723d0e59'
CLIENT_SECRET = 'f301225d3cc3449ba674a36ee64a1cbf'

credentialsManager = \
SpotifyClientCredentials(client_id=CLIENT_ID,
                             client_secret=CLIENT_SECRET)

# sp = spotipy.Spotify(client_credentials_manager=credentialsManager)
token = 'BQDnB8O3Ne7UVzQLgE-jKPgimy670abOAyVhR7dezlF4ALuCbdgU-udUAxdaXZ_z0ZD38Ep-j9hgbKzJC_UWlDFUB-8kWKcGtZSva8kbpH2vjN6gX8LkAbAeOMD70J7aF5nd03-Z0NVk8vN8E0mdi0r-UUXHtdSy0Zo8avhPCyga067AHXjvhC5w8ws'
sp = spotipy.Spotify(auth=token)
print(sp.me())
# endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

# request_body = json.dumps({
#     "name": "Indie bands like Franz Ferdinand and Foals but using Python",
#     "description": "My first programmatic playlist, yooo!",
#     "public": False
# })
# response = requests.post(url=endpoint_url, data=request_body, headers={"Content-Type": "application/json",
#                                                                        "Authorization": f"Bearer {token}"})

# url = response.json()['external_urls']['spotify']
# print(response.status_code)
