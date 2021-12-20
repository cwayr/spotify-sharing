import requests
import base64

TOKEN_URL = 'https://accounts.spotify.com/api/token'

class SpotifyAPI:

    def __init__(self, client_id, secret_key):
        self.client_id=client_id
        self.secret_key=secret_key
        self.token_url = TOKEN_URL

    def get_token_headers(self):
        client_creds = f"{self.client_id}:{self.secret_key}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return { "Authorization": f"Basic {client_creds_b64.decode()}" }

    def get_token_data(self):
        return { "grant_type": "client_credentials" }

    def authorize(self):
        res = requests.post(self.token_url, data=self.get_token_data(), headers=self.get_token_headers())
        print(res.json())
        self.access_token = res.json()['access_token']
        return True
