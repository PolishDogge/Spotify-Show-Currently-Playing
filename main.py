import requests
import time
from tkinter import Tk, Label
from PIL import ImageTk, Image
from secret import *

lastImage = None
options = {
        "background_color": "magenta",
        "transparent_background": False,
        
        "font_size": 45, # for header, 2nd line is -15 px
        "font_color": "white",
        "font": "Arial", # InputMono Black

        "picture_width": 300,
        "picture_height": 300,
        "window_width": 1500,
        "window_height": 450
}

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
            artists = [artist for artist in response['item']['artists']]
        except TypeError:
            return response_data
        artist_names = ', '.join([artist['name'] for artist in artists])
        if artist_names == '': # I love Spotify
            artist_names = '# Unknown #'

        response_data = {
            "name": response['item']['name'],
            "artists": artist_names,
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
                anchor="center"
            ),
            Label(
                self.root,
                text="placeholder",
                font=(options['font'], options['font_size'] - 15),
                anchor="center"
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
            print('downloaded')

            # Cstm
            img = Image.open("image.png")
            img = img.resize((self.options['picture_width'], self.options['picture_height']), Image.Resampling.LANCZOS)
            img = img.save("image.png")

            img = ImageTk.PhotoImage(Image.open("image.png"))
            self.panel.config(image=img)
            self.panel.image = img
        else:
            #print("Image already up to date")
            pass

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    spotify = Spotify(REFRESH_TOKEN, BASE64_HASH)
    spotify.refresh()
    gui = SpotifyGUI(spotify, options)
    gui.start()
