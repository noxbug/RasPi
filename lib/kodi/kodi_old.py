from lib.subtitle import Subtitle as Subtitle
from time import sleep
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
        try:
            payload = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': id}
            # convert payload to json object and parse as url
            url_param = urllib.parse.urlencode({'request': json.dumps(payload)})
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

    def get_active_player(self):
        try:
            player = self.request('Player.GetActivePlayers')
            return player[0]
        except:
            print('No active players')
            return {}

    def get_item(self):
        try:
            item = self.request('Player.GetItem', {'properties': ['title', 'album', 'artist', 'season', 'episode', 'duration', 'showtitle', 'tvshowid', 'thumbnail', 'file', 'fanart', 'streamdetails'], 'playerid': 1})
            return item['item']
        except:
            print('Can not get item')
            return {}

    def play_pause(self):
        try:
            status = self.request('Player.PlayPause', {'playerid': 1})
            play = bool(status['speed'])
            return play
        except:
            print('Nothing playing')
            return False

    def stop(self):
        try:
            self.request('Player.Stop', {'playerid': 1})
        except:
            pass

    def get_position(self):
        try:
            position = self.request('Player.GetProperties', {'playerid': 1, 'properties': ['percentage']})
            return position
        except:
            return {}

    def fast_forward(self):
        try:
            position = self.request('Player.Seek', {'playerid': 1, 'value': 'smallforward'})
            return position
        except:
            return {}

    def fast_rewind(self):
        try:
            position = self.request('Player.Seek', {'playerid': 1, 'value': 'smallbackward'})
            return position
        except:
            return {}

    def input_up(self):
        try:
            self.request('Input.Up')
        except:
            pass

    def input_down(self):
        try:
            self.request('Input.Down')
        except:
            pass

    def input_left(self):
        try:
            self.request('Input.Left')
        except:
            pass

    def input_right(self):
        try:
            self.request('Input.Right')
        except:
            pass

    def input_select(self):
        try:
            self.request('Input.Select')
        except:
            pass

    def input_back(self):
        try:
            self.request('Input.Back')
        except:
            pass

    def input_home(self):
        try:
            self.request('Input.Home')
        except:
            pass

    def input_context_menu(self):
        try:
            self.request('Input.ContextMenu')
        except:
            pass

    def input_info(self):
        try:
            self.request('Input.Info')
        except:
            pass

    def album_art(self):
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

    def translate_subtitle(self):
        try:
            item = self.get_item()
            subtitle = Subtitle()
            subtitle.open(item['file'])
            subtitle.translate()
            sleep(3)
            self.next_subtitle()
        except:
            print('Translation failed')
            pass

    def next_subtitle(self):
        try:
            self.request('Player.SetSubtitle', {'playerid': 1, 'subtitle': 'next', 'enable': True})
        except:
            print('No subtitle found')

if __name__ == '__main__':
    if sys.argv[1] == '-update':
        kodi = Kodi('192.168.1.10')
        print('updating library ...')
        kodi.update_library()