from flask import Flask, render_template
from kodi import Kodi

webapp = Flask(__name__)

@webapp.route('/')
def index():
    kodi = Kodi('192.168.1.10')
    item = kodi.get_item()
    try:
        title = item['label']
        if item['type'] == 'episode':
            artist = item['showtitle']
        else:
            artist = 'unknown'
        album_art_url = kodi.get_album_art()
    except:
        title = 'Nothing playing'
        artist = ''
        album_art_url = ''
    return render_template('index.html', title=title, artist=artist, album_art=album_art_url)

if __name__ == '__main__':
    webapp.run(debug=True, host='0.0.0.0')