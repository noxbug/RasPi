from . import rpc


def up():
    """Toggle fullscreen/GUI"""
    rpc.request('GUI.SetFullscreen')
