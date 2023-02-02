import requests

def refresh(refresh_token, base64):
    query = "https://accounts.spotify.com/api/token"
    response = requests.post(query,
                             data={"grant_type": "refresh_token",
                                   "refresh_token": refresh_token},
                             headers={"Authorization": "Basic " + base64})
    response_json = response.json()
    print(response_json)

    print("The access token expires in " + str(response_json["expires_in"]))
    print("The access token is " + response_json["access_token"])
    return response_json["access_token"]