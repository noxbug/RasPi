from kodi import Kodi
import sqlite3
import os


def get_database(self, item):
    database_path = os.path.expanduser('~') + '/.kodi/userdata/Database/'
    files = os.listdir(database_path)
    if item['type'] == 'episode':
        database = ''


kodi = Kodi('192.168.1.10')
player = kodi.get_active_players()
item = kodi.get_item()
path = kodi.get_path_from_db()



print('pipi')

