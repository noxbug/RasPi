from . import rpc


def get_active_player():
    """Returns all active players"""
    try:
        player = rpc.request('Player.GetActivePlayers')
        return player[0]
    except:
        print('No active player')
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
            properties = ['season', 'episode', 'duration', 'showtitle', 'tvshowid', 'thumbnail', 'file', 'fanart']
        else:
            properties = ['title', 'album', 'artist', 'season', 'episode', 'duration', 'showtitle', 'tvshowid', 'thumbnail', 'file', 'fanart', 'streamdetails']
        # get properties
        item = rpc.request('Player.GetItem', {'playerid': player['playerid'], 'properties': properties})
        return item['item']
    except:
        print('Could not get item')
        return {}


def play_pause():
    """Pauses or unpause playback and returns the new state"""
    try:
        status = rpc.request('Player.PlayPause', {'playerid': get_active_player()['playerid']})
        play = bool(status['speed'])
        return play
    except:
        return False


def stop():
    """Stops playback"""
    try:
        rpc.request('Player.Stop', {'playerid': get_active_player()['playerid']})
    except:
        pass


def get_position():
    try:
        position = rpc.request('Player.GetProperties', {'playerid': get_active_player()['playerid'], 'properties': ['percentage', 'time', 'totaltime']})
        return position
    except:
        return {}


def fast_forward():
    try:
        position = rpc.request('Player.Seek', {'playerid': get_active_player()['playerid'], 'value': 'smallforward'})
        return position
    except:
        return {}


def fast_rewind():
    try:
        position = rpc.request('Player.Seek', {'playerid': get_active_player()['playerid'], 'value': 'smallbackward'})
        return position
    except:
        return {}
