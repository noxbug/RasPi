from kodi import Kodi

kodi = Kodi('192.168.1.10')
help = kodi.help('Player.Stop')
kodi.stop()
position = kodi.fast_forward()
player = kodi.get_active_players()
status = kodi.play_pause()
item = kodi.get_item()
temp = item['streamdetails']

print('pipi')