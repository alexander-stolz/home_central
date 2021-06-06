import time
from flask import Flask, request
from flask.helpers import url_for
from flask.templating import Environment, render_template
from werkzeug.utils import redirect
import telnetlib
from selenium import webdriver
import json
from random import choice
import pynput
from pynput.keyboard import Key
from pynput.mouse import Button
# https://pypi.org/project/pynput/

app = Flask(__name__)
browser = None
keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()

playlists = json.load(open('playlists.json'))

@app.route('/')
def mainpage():
    tiles = dict(
        prismatik=dict(
            prismatik=dict(
                __default='#',
                farbe=url_for('set_prismatik_profile', name='colour'),
                normal=url_for('set_prismatik_profile', name='normal'),
            ),
        ),
        musik=dict(
            pop=url_for('music', genre='pop'),
            tropical_house=url_for('music', genre='tropical_house'),
            off=url_for('music', genre='off')
        ),
        volume=dict(
          vol=dict(
            __default=url_for('volume', volume='toggle_mute'),
            leiser=url_for('volume', volume='-'),
            lauter=url_for('volume', volume='+'),
          ),
        ),
        air_mouse=url_for('airmouse'),
        # ender=url_for('ender'),
    )
    return render_template('index.jinja2', tiles=tiles)


@app.route('/prismatik/profile/<name>')
def set_prismatik_profile(name='colour'):
    with telnetlib.Telnet('192.168.1.108', '3636') as tn:
        tn.write(b'lock\n')
        tn.write(f'setprofile:{name}\n'.encode())
        tn.write(b'unlock\n')
        tn.write(b'exit\n')
    return redirect(url_for('mainpage'))


@app.route('/music/<genre>')
def music(genre:str=None):
    # no default
    global browser
    browser = browser or webdriver.Chrome()
    try:
        if genre == 'off':
            browser.get('about:blank')
        elif genre:
            browser.get(choice(playlists[genre]))
    except:
        browser = None
        return redirect(url_for('music', genre=genre))
    return redirect(url_for('mainpage'))


@app.route('/volume/<volume>')
def volume(volume:str=None):
    # default = toggle mute
    if volume == '+':
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
    elif volume == '-':
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
    else:
        # toggle
        keyboard.press(Key.media_volume_mute)
        keyboard.release(Key.media_volume_mute)
    return redirect(url_for('mainpage'))


@app.route('/airmouse', methods=['GET', 'POST'])
def airmouse():
    if request.method == 'POST':
        res = json.loads(request.get_data())
        dx, dy, touches = res['x'], res['y'], res['touches']
        if dx == dy == 0:
            if touches == 0:
                mouse.click(Button.left)
            elif touches == 1:
                mouse.click(Button.right)
        elif touches == 1:
            mouse.move(dx * 5, dy * 5)
        elif touches == 2:
            if abs(dx) > 2 > abs(dy) * 1:
                mouse.scroll(dx, 0)
            elif abs(dy) > .3 > abs(dx) * 1:
                mouse.scroll(0, dy)
            # else:
            #     mouse.scroll(dx, dy)
        return (
            json.dumps({'success':True}),
            200,
            {'ContentType':'application/json'}
        )
    return render_template('airmouse.html')


@app.route('/airmouse/move')
def airmouse_move():
    return None


@app.route('/ender')
def ender():
    return redirect(url_for('mainpage'))

# python -m pipenv run flask run
if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=False)
