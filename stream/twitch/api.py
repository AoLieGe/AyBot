import requests


class TwitchApi:
    def __init__(self, client_id, secret):
        self.client_id = client_id  #'nworckgcy2tt7drnwfqywhns7vg7nu'
        self.secret = secret  #'pvhgv4ry9t2eor1tkd3iwnrbxz1kvp'

    def access_token(self):
        url = 'https://id.twitch.tv/oauth2/token'
        res = requests.post(url, params={
            'client_id': self.client_id,
            'client_secret': self.secret,
            'grant_type': 'client_credentials'
        })

        if res.status_code == 200 and res.json():
            return res.json().get('access_token')

    def get_streams(self, name):
        url = 'https://api.twitch.tv/helix/streams'

        access_token = self.access_token()
        if not access_token:
            return

        res = requests.get(url, params={'user_login': name}, headers={
            'Authorization': f"Bearer {access_token}",
            'Client-ID': self.client_id
        })

        if res.status_code == 200 and res.json():
            for data in res.json()['data']:
                if data['type'] == 'live' and data['user_login'] == name.lower():
                    return {'status': 'live', 'title': data['title']}
