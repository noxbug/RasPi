import requests
import sqlite3
import urllib
import json
import os

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
            quit()

    def help(self, method):
        info = self.request('JSONRPC.Introspect', {'filter': {'id': method, 'type': 'method'}})
        return info

    def get_active_players(self):
        player = self.request('Player.GetActivePlayers')
        if len(player) == 0:
            print('No active player')
            quit()
        else:
            return player[0]

    def get_item(self):
        player = self.get_active_players()
        item = self.request('Player.GetItem', {'playerid': player['playerid']})
        return item['item']

    def get_path_from_db(self):
        # get item
        item = self.get_item()
        type = item['type']
        if type == 'episode':
            # find name of sql database
            database_path = os.path.expanduser('~') + '/.kodi/userdata/Database/'
            files = os.listdir(database_path)
            for file in files:
                if 'MyVideos' in file:
                    database_name = file
                    break
            # connect to database
            database = sqlite3.connect(database_path + database_name)
            cursor = database.cursor()
            # query database
            query = 'SELECT c18 FROM ' + type + ' WHERE id' + type.capitalize() + '=?'
            id = (str(item['id']),)
            cursor.execute(query, id)
            path = cursor.fetchone()[0]
            return path
        else:
            print('There is no database for this type of media')
            quit()


    def update_library(self):
        self.request('VideoLibrary.Clean')
        self.request('VideoLibrary.Scan')



