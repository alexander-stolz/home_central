from flask import Blueprint, request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from selenium import webdriver
import json
from random import choice

browser = None
playlists = json.load(open('plugins/music/playlists.json'))

plugin_name = 'musik'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            musik=dict(
                __default=url_for('{plugin_name}.music_more'),
                random=url_for('{plugin_name}.music', genre='random'),
                off=url_for('{plugin_name}.music', genre='off')
            )
        )"""

@bp.route('/music/<genre>')
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
        return redirect(url_for(f'{plugin_name}.music', genre=genre))
    return redirect(url_for('mainpage'))


@bp.route('/music')
def music_more():
    tiles = dict(
        back=url_for('mainpage'),
        pop=url_for(f'{plugin_name}.music', genre='pop'),
        tropical_house=url_for(f'{plugin_name}.music', genre='tropical_house'),
        chill=url_for(f'{plugin_name}.music', genre='chill'),
        electroswing=url_for(f'{plugin_name}.music', genre='electroswing'),
        off=url_for(f'{plugin_name}.music', genre='off')
    )
    return render_template('scaffold.jinja2', tiles=tiles)
