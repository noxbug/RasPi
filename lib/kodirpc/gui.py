from . import rpc as _rpc


def up():
    """Toggle fullscreen/GUI"""
    _rpc.request('GUI.SetFullscreen')
