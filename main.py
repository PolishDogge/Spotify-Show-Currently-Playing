import requests
from secret import *
import urllib.request
from PIL import Image
from time import sleep


SPOTIFY_GET_CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player/currently-playing"
current_image_link = None

class spot:                
    def get_current_track(access_token):
        response = requests.get(
            SPOTIFY_GET_CURRENT_TRACK_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        json_resp = response.json()

        track_id = json_resp['item']['id']
        track_name = json_resp['item']['name']
        artists = [artist for artist in json_resp['item']['artists']]
        image = json_resp['item']["album"]["images"][1]["url"]

        link = json_resp['item']['external_urls']['spotify']

        artist_names = ', '.join([artist['name'] for artist in artists])

        current_track_info = {
        	"id": track_id,
        	"track_name": track_name,
        	"artists": artist_names,
        	"link": link,
            "image": image
        }

        return current_track_info


    def update_image(current_track_info):
        global current_image_link
        if current_track_info['image'] != None:
            if current_image_link != current_track_info['image']:
                urllib.request.urlretrieve(current_track_info['image'], "img.png")
                img = Image.open("img.png")
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                img = img.save("img.png")
                print("Image updated")
        current_image_link = current_track_info['image']

ref_count = 0
while True:
    x = spot.get_current_track(access_token)
    spot.update_image(x)

    print('='*10)
    print("Current track: " + x['track_name'])
    print("Artists: " + x['artists'])
    print("Link: " + x['link'])
    print('='*10)
    sleep(5)
    ref_count += 1
    if ref_count == 600:
        access_token = refresh(refresh_token, base64)
        ref_count = 0