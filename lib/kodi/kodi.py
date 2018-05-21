from lib.kodi.rpc import RPC
from lib.kodi.input import Input
from lib.kodi.player import Player
from lib.kodi.helper import Connection


class Kodi:
    def __init__(parent, host='localhost', port=8080):
        parent.host = host
        parent.port = port

        # bind subclasses
        parent.rpc = RPC()
        parent.input = Input()
        parent.player = Player()
