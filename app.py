import time
from flask import Flask, request
from flask.helpers import url_for
from flask.templating import Environment, render_template
from werkzeug.utils import redirect
import telnetlib
from selenium import webdriver
import json
from random import choice

app = Flask(__name__)
browser = None

playlists = json.load(open('playlists.json'))

@app.route('/')
def mainpage():
    tiles = dict(
        prismatik=dict(
            prismatik=dict(
                farbe=url_for('set_prismatik_profile', name='colour'),
                normal=url_for('set_prismatik_profile', name='normal'),
            ),
        ),
        musik=dict(
            pop=url_for('music', genre='pop'),
            tropical_house=url_for('music', genre='tropical_house'),
            off=url_for('music', genre='off')
        ),
        ender=url_for('ender'),
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
def music(genre):
    global browser
    browser = browser or webdriver.Chrome()
    try:
        if genre == 'off':
            browser.get('about:blank')
        else:
            browser.get(choice(playlists[genre]))
    except:
        browser = None
        return redirect(url_for('music', genre=genre))
    return redirect(url_for('mainpage'))


@app.route('/ender')
def ender():
    return redirect(url_for('mainpage'))


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)