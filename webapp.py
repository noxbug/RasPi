from flask import Flask, render_template, redirect, url_for
from kodi import Kodi

webapp = Flask(__name__)

@webapp.route('/')
def index():
    global kodi
    item = kodi.get_item()
    try:
        title = item['label']
        if item['type'] == 'episode':
            artist = item['showtitle']
        else:
            artist = 'unknown'
        album_art_url = kodi.get_album_art()
    except:
        title = 'Nothing Playing'
        artist = 'Unkown'
        album_art_url = '/static/ben.jpg'
        # album_art_url = ''
    return render_template('index.html', title=title, artist=artist, album_art=album_art_url)


@webapp.route('/previous')
def previous():
    return redirect(url_for('index'))


@webapp.route('/play')
def play():
    return redirect(url_for('index'))


@webapp.route('/next')
def next():
    return redirect(url_for('index'))


kodi = Kodi('192.168.1.10')


if __name__ == '__main__':
    webapp.run(debug=True, host='0.0.0.0')