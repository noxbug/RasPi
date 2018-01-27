from kodi import Kodi

kodi = Kodi('192.168.1.10')
info = kodi.help('Player.SetSubtitle')
kodi.set_subtitle()


print('pipi')