from kodi import Kodi

kodi = Kodi('192.168.1.10')
help = kodi.help('Player.GetProperties')
# kodi.stop()
position = kodi.position()
position = kodi.fast_forward()
player = kodi.get_active_players()
status = kodi.play_pause()
item = kodi.get_item()
temp = item['streamdetails']

print('pipi')