from kodi import Kodi

kodi = Kodi('192.168.1.10')
info = kodi.help('Player.SetSubtitle')

path = '/media/pi/hdd/Series/Salamander/S01E01.srt'

file = open(path,'r', encoding='iso-8859-1')

for line in file:
    print(line)

print('pipi')