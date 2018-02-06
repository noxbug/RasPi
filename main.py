from kodi import Kodi

kodi = Kodi('192.168.1.10')
help = kodi.help('Player.PlayPause')
position = kodi.fast_forward()
status = kodi.play_pause()
item = kodi.get_item()

print('pipi')