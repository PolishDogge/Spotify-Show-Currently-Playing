import requests
from secret import *
import urllib.request

from time import sleep
from tkinter import *
from PIL import Image, ImageTk





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
                print('Failed to get current track 10 times in a row')
                print('Exiting program')
                exit()
            spot.get_current_track(access_token)

        try:
            track_id = json_resp['item']['id']
            track_name = json_resp['item']['name']
            artists = [artist for artist in json_resp['item']['artists']]
            image_ = json_resp['item']["album"]["images"][1]["url"]

            link = json_resp['item']['external_urls']['spotify']
            currently_at = json_resp['progress_ms']
            max_duration = json_resp['item']['duration_ms']
            artist_names = ', '.join([artist['name'] for artist in artists])
        except:
            spot.get_current_track(access_token)


        current_track_info = {
        	"id": track_id,
        	"track_name": track_name,
        	"artists": artist_names,
        	"link": link,
            "image": image_,
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
                img = img.resize((150, 150), Image.ANTIALIAS)
                img = img.save("img.png")
                print("Image updated")
        current_image_link = current_track_info['image']



def convert_to_minutes(seconds):
    seconds = int(seconds)
    minutes = seconds // 60000
    seconds = seconds % 60000
    seconds = seconds // 1000
    if seconds < 10:
        seconds = '0' + str(seconds)
    return str(minutes) + ':' + str(seconds)

# set up tkinter

root = Tk()
root.configure(bg='green')

#set white to be transparent
root.attributes('-transparentcolor','green')

root.geometry("500x300")
img = ImageTk.PhotoImage(Image.open("img.png"))
root.title("Spotify Now Playing")

panel = Label(root, image = img)
panel.grid(row=0,column=0, rowspan=3, columnspan=3)


# set up labels 
l1 = Label(root, text = "placeholder", font=("Arial", 30))
l2 = Label(root, text = "placeholder 2", font=("Arial", 30))
l1.grid(row = 1, column = 3, sticky=N)
l2.grid(row = 2, column = 3, sticky=N)
l1.configure(bg='green', fg='white')
l2.configure(bg='green', fg='white')
ref_count = 0

def update_image():
    global l1, l2, panel, img, x, ref_count, access_token
    x = spot.get_current_track(access_token)
    spot.update_image(x)
    img = ImageTk.PhotoImage(Image.open("img.png"))
    l1.configure(text=x['track_name'])
    l2.configure(text=x['artists'])
    panel.configure(image=img)
    print("Updated")
    ref_count += 1
    print(f'{ref_count} / 400')
    if ref_count == 400:
        access_token = refresh(refresh_token, base64)
        ref_count = 0
    root.after(10000, update_image)


while True:
    global x
    x = spot.get_current_track(access_token)
    spot.update_image(x)

    # this is a text version of the program

    #x['currently_at'] = convert_to_minutes(x['currently_at'])
    #x['max_duration'] = convert_to_minutes(x['max_duration'])
    #print('='*10)
    #print("Current track: " + x['track_name'])
    #print("Artists: " + x['artists'])
    #print("Link: " + x['link'])
    #print(f"Currently at: {x['currently_at']} / {x['max_duration']}")
    #print('='*10)
    #sleep(5)
    #ref_count += 1
    #if ref_count == 600:
    #    access_token = refresh(refresh_token, base64)
    #    ref_count = 0
    
    root.after(5000, update_image)
    root.mainloop()