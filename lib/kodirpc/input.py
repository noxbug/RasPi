from . import rpc


def up():
    """Navigate up in GUI"""
    rpc.request('Input.Up')


def down():
    """Navigate down in GUI"""
    rpc.request('Input.Down')


def left():
    """Navigate left in GUI"""
    rpc.request('Input.Left')


def right():
    """Navigate right in GUI"""
    rpc.request('Input.Right')


def select():
    """Select current item in GUI"""
    rpc.request('Input.Select')


def back():
    """Goes back in GUI"""
    rpc.request('Input.Back')


def home():
    """Goes to home window in GUI"""
    rpc.request('Input.Home')


def context_menu():
    """Shows the context menu"""
    rpc.request('Input.ContextMenu')


def info():
    """Shows the information dialog"""
    rpc.request('Input.Info')
