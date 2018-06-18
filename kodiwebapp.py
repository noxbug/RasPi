from flask import Flask, render_template, redirect, request, url_for
import lib.kodirpc as kodi

app = Flask(__name__)

kodi.connection.new('192.168.1.10')

@app.route('/')
@app.route('/index')
def index():
    kodi.nowplaying.update()
    return render_template('now_playing.html', kodi=kodi)


### PLAYER ###
@app.route('/play')
def play():
    kodi.player.play_pause()
    return redirect(request.referrer)


@app.route('/stop')
def stop():
    kodi.player.stop()
    return redirect(url_for('index'))


@app.route('/next')
def next():
    kodi.player.fast_forward()
    return redirect(url_for('index'))


@app.route('/previous')
def previous():
    kodi.player.fast_rewind()
    return redirect(url_for('index'))


### REMOTE ###
@app.route('/remote')
def remote():
    return render_template('remote.html', kodi=kodi)


@app.route('/up')
def up():
    kodi.input.up()
    return redirect(url_for('remote'))


@app.route('/down')
def down():
    kodi.input.down()
    return redirect(url_for('remote'))


@app.route('/left')
def left():
    kodi.input.left()
    return redirect(url_for('remote'))


@app.route('/right')
def right():
    kodi.input.right()
    return redirect(url_for('remote'))


@app.route('/select')
def select():
    kodi.input.select()
    return redirect(url_for('remote'))


@app.route('/back')
def back():
    kodi.input.back()
    return redirect(url_for('remote'))


@app.route('/home')
def home():
    kodi.input.home()
    return redirect(url_for('remote'))


@app.route('/context_menu')
def context_menu():
    kodi.input.context_menu()
    return redirect(url_for('remote'))


@app.route('/info')
def info():
    kodi.input.info()
    return redirect(url_for('remote'))


### DROPDOWN MENU ###
@app.route('/translate_sub')
def translate_sub():
    return redirect(url_for('index'))


@app.route('/next_sub')
def next_sub():
    return redirect(url_for('index'))


@app.route('/update')
def update():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')