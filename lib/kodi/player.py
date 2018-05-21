from lib.kodi.rpc import RPC


class Player:
    def __init__(self, connection):
        self._rpc = RPC(connection)

    def get_active_player(self):
        player = self._rpc.request('Player.GetActivePlayers')
        return player[0]

    def get_item(self):
        # get active playerid + content type
        player = self.get_active_player()
        # select which poroperties
        if player['type'] == 'audio':
            properies = ['title', 'artist', 'album', 'duration','thumbnail', 'file', 'fanart']
        elif player['type'] == 'video':
            properies = ['season', 'episode', 'duration', 'showtitle', 'tvshowid', 'thumbnail', 'file', 'fanart']
        else:
            properies = ['title', 'album', 'artist', 'season', 'episode', 'duration', 'showtitle', 'tvshowid', 'thumbnail', 'file', 'fanart', 'streamdetails']

        item = self._rpc.request('Player.GetItem', {'properties': properies, 'playerid': player['playerid']})
        return item['item']

    def play_pause(self):
        status = self._rpc.request('Player.PlayPause', {'playerid': self.get_active_player()['playerid']})
        play = bool(status['speed'])
        return play

    def stop(self):
        self._rpc.request('Player.Stop', {'playerid': self.get_active_player()['playerid']})

    def get_position(self):
        position = self._rpc.request('Player.GetProperties', {'playerid': self.get_active_player()['playerid'], 'properties': ['percentage']})
        return position

    def fast_forward(self):
        position = self._rpc.request('Player.Seek', {'playerid': self.get_active_player()['playerid'], 'value': 'smallforward'})
        return position

    def fast_rewind(self):
        position = self._rpc.request('Player.Seek', {'playerid': self.get_active_player()['playerid'], 'value': 'smallbackward'})
        return position
