import requests
import urllib
import json
import sys

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
            print('Error: can not connect to Kodi')
            return {}

    def help(self, method):
        info = self.request('JSONRPC.Introspect', {'filter': {'id': method, 'type': 'method'}})
        return info

    def get_active_players(self):
        player = self.request('Player.GetActivePlayers')
        try:
            return player[0]
        except:
            print('No active players')
            return {}

    def next_subtitle(self):
        player = self.get_active_players()
        self.request('Player.SetSubtitle', {'playerid': player['playerid'], 'subtitle': 'next', 'enable': True})

    def get_item(self):
        try:
            player = self.get_active_players()
            # item = self.request('Player.GetItem', {'playerid': player['playerid']})
            item = self.request('Player.GetItem', {'properties': ['title', 'album', 'artist', 'season', 'episode', 'duration', 'showtitle', 'tvshowid', 'thumbnail', 'file', 'fanart', 'streamdetails'], 'playerid': player['playerid']})
            return item['item']
        except:
            print('Can not get item')
            return {}

    def get_album_art(self):
        try:
            item = self.get_item()
            album_art = self.request('Files.PrepareDownload', {'path': item['thumbnail']})
            album_art_url = 'http://' + self.host + ':' + str(self.port) + '/' + album_art['details']['path']
            return album_art_url
        except:
            print('Can not get album art url')
            return ''

    def update_library(self):
        self.request('VideoLibrary.Clean')
        self.request('VideoLibrary.Scan')

if __name__ == '__main__':
    if sys.argv[1] == '-update':
        kodi = Kodi('192.168.1.10')
        print('updating library ...')
        kodi.update_library()