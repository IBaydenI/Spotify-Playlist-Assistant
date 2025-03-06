"""
This class takes care of authenticating the user to the Spotify API.
It is using the Authorization code PKCE method from Spotifys API documentation https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow
"""

import secrets
import string
import hashlib
import base64
import requests

"""
Input: length of the string to be generated
Output: random string of length "length"
"""
def generateRandomString(length):
    random_string = ""
    for i in range(length):
        random_string += (secrets.choice(string.ascii_letters + string.digits + "-" + "_" + "."))
    return random_string

def SpotifyAuthorization():
    clientID = "" # From Spotify developer portal
    authorizationEndpoint = "https://accounts.spotify.com/authorize"
    tokenEndpoint = "https://accounts.spotify.com/api/token"
    scope = 'playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public'

    codeVerifier = generateRandomString(64)
    codeVerifier_hashed = hashlib.sha256(codeVerifier.encode('ascii')).digest()
    codeVerifier_base64 = base64.b64encode(codeVerifier_hashed).decode("ascii")

    params = {
        "response_type": 'code',
        "client_id": clientID,
        "scope": scope,
        "code_challenge_method": 'S256',
        "code_challenge": codeVerifier_base64
    }
    getReq = requests.get(authorizationEndpoint, params)
    print(getReq.status_code)

SpotifyAuthorization()