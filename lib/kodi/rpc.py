import requests
import urllib
import json


class RPC:
    def __init__(self):
        self.headers = {'content-type': 'application/json'}
        self.url = 'http://' + parent.host + ":" + str(parent.port) + '/jsonrpc'

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
