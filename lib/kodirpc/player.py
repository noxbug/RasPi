from . import connection
from . import nowplaying
from . import rpc

def get_active_player():
    """Returns all active players"""
    try:
        player = rpc.request('Player.GetActivePlayers')
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
        item = rpc.request('Player.GetItem', {'playerid': player['playerid'], 'properties': properties})
        return item['item']
    except:
        print('WARNING: Could not get item')
        return {}


def get_album_art_url():
    try:
        item = get_item()
        album_art = rpc.request('Files.PrepareDownload', {'path': item['thumbnail']})
        album_art_url = 'http://' + connection.host + ':' + str(connection.port) + '/' + album_art['details']['path']
        return album_art_url
    except:
        return ''


def play_pause():
    """Pauses or unpause playback and returns the new state"""
    try:
        playerid = get_active_player()['playerid']
        status = rpc.request('Player.PlayPause', {'playerid': playerid})
        play = bool(status['speed'])
        return play
    except:
        return False


def stop():
    """Stops playback"""
    try:
        playerid = get_active_player()['playerid']
        rpc.request('Player.Stop', {'playerid': playerid})
    except:
        pass


def get_position():
    try:
        playerid = get_active_player()['playerid']
        position = rpc.request('Player.GetProperties', {'playerid': playerid, 'properties': ['percentage', 'time', 'totaltime', 'speed']})
        return position
    except:
        return {}


def fast_forward():
    try:
        playerid = get_active_player()['playerid']
        position = rpc.request('Player.Seek', {'playerid': playerid, 'value': 'smallforward'})
        return position
    except:
        return {}


def fast_rewind():
    try:
        playerid = get_active_player()['playerid']
        position = rpc.request('Player.Seek', {'playerid': playerid, 'value': 'smallbackward'})
        return position
    except:
        return {}
