from lib.kodi import Kodi as Kodi

kodi = Kodi('192.168.1.10')
help = kodi.help('Player.GetProperties')
kodi.input_left()
# kodi.stop()
position = kodi.position()
position = kodi.fast_forward()
player = kodi.active_player()
status = kodi.play_pause()
item = kodi.item()
temp = item['streamdetails']

print('pipi')