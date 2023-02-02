from refresh import refresh

#https://accounts.spotify.com/authorize?client_id=8d000b873e3047c5a0cb1c1c32ca1d12&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2FPolishDogge&scope=user-read-playback-state

spotify_id = ''
refresh_token = ''
base64 = ''
access_token = refresh(refresh_token, base64)
