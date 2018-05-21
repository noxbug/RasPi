from . import rpc


def update():
    """
    Cleans the library from non-existent items
    Scans the audio sources for new library items
    """
    rpc.request('AudioLibrary.Clean')
    rpc.request('VideoLibrary.Clean')
    rpc.request('AudioLibrary.Scan')
    rpc.request('VideoLibrary.Scan')