from kodi import Kodi

kodi = Kodi('192.168.1.10')
help = kodi.help('Player.GetItem')
player = kodi.get_active_players()
item = kodi.get_item()
album_art_url = kodi.get_album_art()
#album_url = item['thumbnail']

print('pipi')