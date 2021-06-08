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
blocked_until = 0

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
            musik=dict(
                __default=url_for('music_more'),
                random=url_for('music', genre='random'),
                off=url_for('music', genre='off')
            )
        ),
        volume=dict(
          vol=dict(
            __default=url_for('volume', volume='toggle_mute'),
            leiser=url_for('volume', volume='-'),
            lauter=url_for('volume', volume='+'),
          ),
        ),
        ender=dict(
            ender=dict(
                __default=url_for('ender_more'),
                home=url_for('ender', cmd='home'),
                up=url_for('ender', cmd='move_up'),
                cancel=url_for('ender', cmd='cancel'),
            ),
        ),
        air_mouse=url_for('airmouse'),
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
        elif genre == 'random':
            _genre = choice(tuple(playlists.keys()))
            _pl = choice(playlists[_genre])
            browser.get(_pl)
        elif genre:
            browser.get(choice(playlists[genre]))
    except Exception as e:
        print(e)
        browser = None
        return redirect(url_for('music', genre=genre))
    return redirect(url_for('mainpage'))


@app.route('/music')
def music_more():
    tiles = dict(
        back=url_for('mainpage'),
        pop=url_for('music', genre='pop'),
        tropical_house=url_for('music', genre='tropical_house'),
        chill=url_for('music', genre='chill'),
        electroswing=url_for('music', genre='electroswing'),
        off=url_for('music', genre='off')
    )
    return render_template('index.jinja2', tiles=tiles)


@app.route('/volume/<volume>')
def volume(volume:str=None):
    # default = toggle mute
    if volume == '+':
        for _ in range(2):
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
    elif volume == '-':
        for _ in range(2):
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
    else:
        # toggle
        keyboard.press(Key.media_volume_mute)
        keyboard.release(Key.media_volume_mute)
    return redirect(url_for('mainpage'))


@app.route('/airmouse', methods=['GET', 'POST'])
def airmouse():
    def block_mouse(dt):
        global blocked_until
        blocked_until = time.perf_counter() + dt

    def mouse_blocked():
        return time.perf_counter() < blocked_until

    if request.method == 'POST':
        res = json.loads(request.get_data())
        dx, dy, touches = res['x'], res['y'], res['touches']
        if dx == dy == 0 and not mouse_blocked():
            if touches == 0:
                mouse.click(Button.left)
            elif touches == 1:
                mouse.click(Button.right)
        elif touches == 1 and not mouse_blocked():
            mouse.move(dx * 5, dy * 5)
        elif touches == 2:
            if abs(dx) > 2 > abs(dy) * 1:
                mouse.scroll(dx, 0)
            elif abs(dy) > abs(dx) * 1:
                mouse.scroll(0, dy / 3)
            block_mouse(dt=.3)
            # else:
            #     mouse.scroll(dx, dy)
        return (
            json.dumps({'success':True}),
            200,
            {'ContentType':'application/json'}
        )
    return render_template('airmouse.html')


@app.route('/ender/<cmd>')
def ender(cmd):
    import ender
    if cmd == 'cancel':
        ender.cancel()
    elif cmd == 'move_up':
        ender.send_gcode('G1 Z100')
    elif cmd == 'home':
        ender.send_gcode('G28')
    return redirect(url_for('mainpage'))


@app.route('/ender')
def ender_more():
    tiles = dict(
        back=url_for('mainpage'),
        control=dict(
            control=dict(
                cancel=url_for('ender', cmd='cancel'),
                pause=url_for('ender', cmd='pause'),
                up=url_for('ender', cmd='move_up'),
            ),
        ),
        bed=dict(
            bed=dict(
                heat=url_for('ender', cmd='bed_heat'),
                off=url_for('ender', cmd='bed_off'),
            )
        ),
        tool=dict(
            tool=dict(
                heat=url_for('ender', cmd='tool_heat'),
                off=url_for('ender', cmd='tool_off'),
            ),
        )
    )
    return render_template('index.jinja2', tiles=tiles)


# python -m pipenv run flask run
if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=False)
