import requests
import json
import urllib

class Kodi:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.headers = {'content-type': 'application/json'}
        self.url = 'http://' + host + ":" + str(port) + '/jsonrpc'

    def request(self, method, params={}, id=1):
        payload = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': id}
        # convert payload to json object and parse as url
        url_param = urllib.parse.urlencode({'request': json.dumps(payload)})
        try:
            # contact server
            json_response = requests.get(self.url + '?' + url_param, headers=self.headers)
            # json object to python
            response = json.loads(json_response.text)
            return response['result']
        except:
            print('Error: can not connect to Kodi, is Kodi running?')
            quit()

    def get_active_players(self):
        player = self.request('Player.GetActivePlayers')
        if len(player) == 0:
            print('No active player')
            return {'playerid': -1}
        else:
            return player[0]

    def get_item(self):
        player = self.get_active_players()
        if player['playerid'] == -1:
            return ''
        else:
            item = self.request('Player.GetItem', {'playerid': player['playerid']}, 'VideoGetItem')
            return item['item']['label']

    def update_library(self):
        self.request('VideoLibrary.Clean')
        self.request('VideoLibrary.Scan')



