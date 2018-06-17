from . import rpc as _rpc
from . import nowplaying as _nowplaying

def up():
    """Navigate up in GUI"""
    _rpc.request('Input.Up')


def down():
    """Navigate down in GUI"""
    _rpc.request('Input.Down')


def left():
    """Navigate left in GUI"""
    _rpc.request('Input.Left')


def right():
    """Navigate right in GUI"""
    _rpc.request('Input.Right')


def select():
    """Select current item in GUI"""
    _rpc.request('Input.Select')
    _nowplaying.update()


def back():
    """Goes back in GUI"""
    _rpc.request('Input.Back')


def home():
    """Goes to home window in GUI"""
    _rpc.request('Input.Home')


def context_menu():
    """Shows the context menu"""
    _rpc.request('Input.ContextMenu')


def info():
    """Shows the information dialog"""
    _rpc.request('Input.Info')
