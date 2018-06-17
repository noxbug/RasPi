from . import rpc as _rpc


def update():
    """
    Cleans the library from non-existent items
    Scans the audio sources for new library items
    """
    _rpc.request('AudioLibrary.Clean')
    _rpc.request('VideoLibrary.Clean')
    _rpc.request('AudioLibrary.Scan')
    _rpc.request('VideoLibrary.Scan')