from . import connection
import requests
import urllib
import json


def request(method, params={}, id=1):
    try:
        # construct url
        headers = {'content-type': 'application/json'}
        url = 'http://' + connection.host + ":" + str(connection.port) + '/jsonrpc'
        # generate payload
        payload = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': id}
        # convert payload to json object and parse as url
        url_param = urllib.parse.urlencode({'request': json.dumps(payload)})
        # contact server
        json_response = requests.get(url + '?' + url_param, headers=headers)
        # json object to python
        response = json.loads(json_response.text)
        return response['result']
    except:
        print('ERROR: can not connect to Kodi')
        return {}

def help(method):
    """Enumerates all actions and descriptions"""
    info = request('JSONRPC.Introspect', {'filter': {'id': method, 'type': 'method'}})
    return info

def ping():
    """Ping responder"""
    ping = request('JSONRPC.Ping')
    return ping
