import requests
import time
from tkinter import Tk, Label
from PIL import ImageTk, Image
import json
import base64
from pathlib import Path
import os

CURRENT_PLAYING_URL = 'https://api.spotify.com/v1/me/player/currently-playing'

def setUp():
    client_id = ''
    redirect = 'https://github.com/PolishDogge/Spotify-Show-Currently-Playing/README.md'
    client_secret = ''

    print(f'Authorize the app and follow the given instruction\n \nhttps://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect}&scope=user-read-currently-playing')
    cde = input('Put the obtained code here\n')
    tokenlink = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': cde,
        'redirect_uri': redirect,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    respon = requests.post(tokenlink, data=payload)
    
    if respon.status_code == 200:
        response_data = respon.json()
        access_token = response_data.get('access_token')
        refresh_token = response_data.get('refresh_token')
        base64_hash = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        op = {
            "refresh_token": refresh_token,
            "base64_hash": base64_hash
        }
        appdata_dir = Path(os.getenv('LOCALAPPDATA')) / 'CurrentlyPlaying'
        appdata_dir.mkdir(parents=True, exist_ok=True)
        sav = appdata_dir / 'secret.txt'
        with open(sav, 'w') as s:
            json.dump(op, s, indent=4)
    else:
        print("Failed to obtain tokens")
        print(respon.text)
        exit()

try:
    appdata_dir = Path(os.getenv('LOCALAPPDATA')) / 'CurrentlyPlaying'
    appdata_dir.mkdir(parents=True, exist_ok=True)
    sav = appdata_dir / 'secret.txt'
    with open(sav,'r') as sec:
        secrets = json.load(sec)
        sec.close()
except FileNotFoundError:
    setUp()
    print('Press ENTER to finish setup and restart the app.')
    input()
    exit()


try:
    with open('options.txt', 'r') as opt:
        options = json.load(opt)
        print('loaded options file')
except (FileNotFoundError, json.JSONDecodeError):
    options = {
        "background_color": "magenta",
        "transparent_background": False,
        "font_size": 45,
        "font_color": "white",
        "font": "InputMono Black",
        "picture_width": 300,
        "picture_height": 300,
        "window_width": 1500,
        "window_height": 550
    }
    with open('options.txt', 'w') as s:
        json.dump(options, s, indent=4)



lastImage = None
class Spotify:
    def __init__(self, refresh_token, base64_hash):
        self.refresh_token = refresh_token
        self.base64_hash = base64_hash
        self.access_token = None
        self.token_generated_at = None
        self.token_expires_in = None

    def get_currently_playing(self):
        response = requests.get(
            CURRENT_PLAYING_URL, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response = response.json()
        try:
            if response is None:
                return response_data
            artists = [artist for artist in response['item']['artists']] 
        except (TypeError, KeyError): # why tho
            return response_data
        

        artist_names = ', '.join([artist['name'] for artist in artists])
        if artist_names == '': # I love Spotify
            artist_names = '# Unknown #'

        response_data = {
            "name": response['item']['name'],
            "artists": f'By {artist_names}',
            "imageLink": response['item']["album"]["images"][1]["url"],
        }
        return response_data

    def refresh(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query, data={
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }, headers={
            "Authorization": f"Basic {self.base64_hash}"
        })
        response_json = response.json()
        self.access_token = response_json.get("access_token")
        self.token_generated_at = int(time.time())
        self.token_expires_in = response_json.get("expires_in")

    def is_token_expired(self):
        if self.token_generated_at is None or self.token_expires_in is None:
            return True

        current_time = int(time.time())
        expiration_time = self.token_generated_at + self.token_expires_in - 300
        return current_time >= expiration_time

class SpotifyGUI:
    def __init__(self, spotify, options):
        self.spotify = spotify
        self.options = options

        self.root = Tk()
        self.root.geometry(f"{options['window_width']}x{options['window_height']}")
        self.root.title("Spotify Now Playing")
        self.root.configure(bg=options['background_color'])

        if options['transparent_background']:
            self.root.attributes('-transparentcolor', options['background_color'])

        self.panel = Label(self.root)
        self.panel.grid(row=0, column=0, rowspan=3, columnspan=3, padx=10, pady=10)
        self.panel.config(bd=0, highlightthickness=2 , highlightcolor='black', highlightbackground='black')

        self.labels = [
            Label(
                self.root,
                text="placeholder",
                font=(options['font'], options['font_size']),
                anchor="center",
            ),
            Label(
                self.root,
                text="placeholder",
                font=(options['font'], options['font_size'] - 15),
                anchor="center",
            )
        ]

        for i, label in enumerate(self.labels):
            label.grid(row=i + 1, column=3, sticky="n")
            label.configure(bg=options['background_color'], fg=options['font_color'], wraplength=int(options["window_width"]*0.7))

        self.update_tk()

    def update_tk(self):
        song_data = self.spotify.get_currently_playing()
        self.update_image(song_data)
        self.labels[0].config(text=song_data["name"])
        self.labels[1].config(text=song_data["artists"])

        if self.spotify.is_token_expired():
            self.spotify.refresh()
            print('Updated access token')
        self.root.after(5000, self.update_tk)

    def update_image(self, data):
        global lastImage
        if lastImage != data["imageLink"]:
            lastImage = data["imageLink"]
            image = requests.get(data["imageLink"])
            with open('image.png', 'wb') as file:
                file.write(image.content)
            img = Image.open("image.png")
            img = img.resize((self.options['picture_width'], self.options['picture_height']), Image.Resampling.LANCZOS)
            img = img.save("image.png")
            img = ImageTk.PhotoImage(Image.open("image.png"))
            self.panel.config(image=img)
            self.panel.image = img
        else:
            pass

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    spotify = Spotify(secrets['refresh_token'],secrets['base64_hash'])
    spotify.refresh()
    gui = SpotifyGUI(spotify, options)
    gui.start()
