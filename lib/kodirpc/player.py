from . import connection as _connection
from . import nowplaying as _nowplaying
from . import rpc as _rpc

def get_active_player():
    """Returns all active players"""
    try:
        player = _rpc.request('Player.GetActivePlayers')
        return player[0]
    except:
        print('WARNING: No active player')
        return {}


def get_item():
    """Retrieves the currently played item"""
    try:
        # get active playerid + content type
        player = get_active_player()
        # select which properties
        if player['type'] == 'audio':
            properties = ['title', 'artist', 'album', 'duration','thumbnail', 'file', 'fanart']
        elif player['type'] == 'video':
            properties = ['title', 'season', 'episode', 'duration', 'showtitle', 'tvshowid', 'thumbnail', 'file', 'fanart']
        else:
            properties = ['title', 'album', 'artist', 'season', 'episode', 'duration', 'showtitle', 'tvshowid', 'thumbnail', 'file', 'fanart', 'streamdetails']
        # get properties
        item = _rpc.request('Player.GetItem', {'playerid': player['playerid'], 'properties': properties})
        return item['item']
    except:
        print('WARNING: Could not get item')
        return {}


def get_album_art_url():
    try:
        item = get_item()
        album_art = _rpc.request('Files.PrepareDownload', {'path': item['thumbnail']})
        album_art_url = 'http://' + _connection.host + ':' + str(_connection.port) + '/' + album_art['details']['path']
        return album_art_url
    except:
        return ''


def play_pause():
    """Pauses or unpause playback and returns the new state"""
    try:
        playerid = get_active_player()['playerid']
        status = _rpc.request('Player.PlayPause', {'playerid': playerid})
        play = bool(status['speed'])
        _nowplaying.update()
        return play
    except:
        _nowplaying.reset()
        return False


def stop():
    """Stops playback"""
    try:
        playerid = get_active_player()['playerid']
        _rpc.request('Player.Stop', {'playerid': playerid})
        _nowplaying.reset()
    except:
        _nowplaying.reset()
        pass


def get_position():
    try:
        playerid = get_active_player()['playerid']
        position = _rpc.request('Player.GetProperties', {'playerid': playerid, 'properties': ['percentage', 'time', 'totaltime', 'speed']})
        return position
    except:
        return {}


def go_to_next():
    try:
        player = get_active_player()
        _rpc.request('Player.GoTo', {'playerid': player['playerid'], 'to': 'next'})
        _nowplaying.update()
    except:
        _nowplaying.reset()
        pass


def go_to_previous():
    try:
        player = get_active_player()
        _rpc.request('Player.GoTo', {'playerid': player['playerid'], 'to': 'previous'})
        _nowplaying.update()
    except:
        _nowplaying.reset()
        pass


def fast_forward():
    try:
        player = get_active_player()
        if player['type'] == 'audio':
            go_to_next()
            position = get_position()
        else:
            position = _rpc.request('Player.Seek', {'playerid': player['playerid'], 'value': 'smallforward'})
            _nowplaying.update()
        return position
    except:
        _nowplaying.reset()
        return {}


def fast_rewind():
    try:
        player = get_active_player()
        if player['type'] == 'audio':
            go_to_previous()
            position = get_position()
        else:
            position = _rpc.request('Player.Seek', {'playerid': player['playerid'], 'value': 'smallbackward'})
            _nowplaying.update()
        return position
    except:
        _nowplaying.reset()
        return {}
