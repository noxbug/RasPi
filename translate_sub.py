from subtitle import Subtitle
from kodi import Kodi

kodi = Kodi('192.168.1.10')
path = kodi.get_path_from_db()

subtitle = Subtitle()
subtitle.open(path)
subtitle.translate()