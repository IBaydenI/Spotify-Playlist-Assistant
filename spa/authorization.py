"""
This class takes care of authenticating the user to the Spotify API.
It is using the Authorization code PKCE method from Spotifys API documentation https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow
"""

import secrets
import string
import hashlib
import base64
import requests
import urllib
import webbrowser

"""
Input: length of the string to be generated
Output: random string of length "length"
"""
def generateRandomString(length):
    random_string = ""
    for i in range(length):
        random_string += (secrets.choice(string.ascii_letters + string.digits + "-" + "_" + "."))
    return random_string

def getCodeChallenge():
    codeVerifier = generateRandomString(64)
    codeVerifier_hashed = hashlib.sha256(codeVerifier.encode('utf-8')).digest()
    codeVerifier_base64 = base64.urlsafe_b64encode(codeVerifier_hashed).decode("utf-8")
    codeVerifier_base64 = codeVerifier_base64.replace('=', '')
    return codeVerifier_base64

def SpotifyAuthorization():
    clientID = "" # From Spotify developer portal
    redirectUri = 'http://127.0.0.1:8080'
    state = None
    authorizationEndpoint = "https://accounts.spotify.com/authorize"
    tokenEndpoint = "https://accounts.spotify.com/api/token"
    # TO-DO! fix passing scope in get request (currently error message is "Illegal scope")
    scope = ("playlist-read-private", "playlist-read-collaborative", "playlist-modify-private", "playlist-modify-public")

    code_challenge = getCodeChallenge()

    payload = { # parameters for get request
        "client_id": clientID,
        "response_type": 'code',
        "redirect_uri": redirectUri,
        "code_challenge_method": 'S256',
        "code_challenge": code_challenge,
        "state": state,
    }
    urlparams = urllib.parse.urlencode(payload)
    getReq = requests.get(authorizationEndpoint, params=urlparams) # send get request and save response

    # open URL returned from request in webbrowser. This is necessary for user authentication
    webbrowser.open_new(getReq.url)



SpotifyAuthorization()