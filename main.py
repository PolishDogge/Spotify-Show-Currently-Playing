import requests
from secret import *
import urllib.request
from PIL import Image
from time import sleep


SPOTIFY_GET_CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player/currently-playing"
current_image_link = None

failed_amount = 0

class spot:                
    def get_current_track(access_token):
        global failed_amount
        response = requests.get(
            SPOTIFY_GET_CURRENT_TRACK_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        try:
            json_resp = response.json()
            failed_amount = 0
        except:
            failed_amount += 1
            print("Error: " + str(response.status_code))
            print('Retrying...')
            sleep(1)
            if failed_amount > 5:
                print('Try to stop and start music on spotify')
            if failed_amount > 10:
                print('Exiting program')
                exit()
            spot.get_current_track(access_token)


        track_id = json_resp['item']['id']
        track_name = json_resp['item']['name']
        artists = [artist for artist in json_resp['item']['artists']]
        image = json_resp['item']["album"]["images"][1]["url"]

        link = json_resp['item']['external_urls']['spotify']
        currently_at = json_resp['progress_ms']
        max_duration = json_resp['item']['duration_ms']
        artist_names = ', '.join([artist['name'] for artist in artists])

        current_track_info = {
        	"id": track_id,
        	"track_name": track_name,
        	"artists": artist_names,
        	"link": link,
            "image": image,
            "currently_at": currently_at,
            "max_duration": max_duration,
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



def convert_to_minutes(seconds):
    seconds = int(seconds) / 1000
    minutes = seconds / 60
    seconds = seconds - (int(minutes) * 60)
    final = f'{int(minutes)}:{int(seconds)}'
    return final

ref_count = 0
while True:
    x = spot.get_current_track(access_token)
    spot.update_image(x)
    x['currently_at'] = convert_to_minutes(x['currently_at'])
    x['max_duration'] = convert_to_minutes(x['max_duration'])

    print('='*10)
    print("Current track: " + x['track_name'])
    print("Artists: " + x['artists'])
    print("Link: " + x['link'])
    print(f"Currently at: {x['currently_at']} / {x['max_duration']}")
    print('='*10)
    sleep(5)
    ref_count += 1
    if ref_count == 600:
        access_token = refresh(refresh_token, base64)
        ref_count = 0
