from flask import Blueprint, request, flash
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from selenium import webdriver
import json
from random import choice
import time

browser = None
playlists = json.load(open('plugins/music/playlists.json'))

plugin_name = 'musik'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            musik=dict(
                __default=url_for('{plugin_name}.music_more'),
                random=url_for('{plugin_name}.music', genre='random'),
                next=url_for('{plugin_name}.music', genre='next'),
                off=url_for('{plugin_name}.music', genre='off')
            )
        )"""

x_path_menu = '/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-browse-response/div[2]/ytmusic-detail-header-renderer/div/ytmusic-menu-renderer/tp-yt-paper-icon-button/tp-yt-iron-icon'
x_path_radio = '/html/body/ytmusic-app/ytmusic-popup-container/tp-yt-iron-dropdown/div/ytmusic-menu-popup-renderer/tp-yt-paper-listbox/ytmusic-menu-navigation-item-renderer[1]/a/yt-formatted-string'
x_path_playpause = '/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[2]/tp-yt-iron-icon'
x_path_next = '/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[3]/tp-yt-iron-icon'

@bp.route('/music/<genre>')
def music(genre:str=None):
    global browser
    if browser:
        try:
            browser.execute_script("window.onbeforeunload = null;")
            browser.execute_script("window.alert = null;")
            browser.find_element_by_xpath(x_path_playpause).click()
        except:
            pass
    browser = browser or webdriver.Chrome()
    if genre == 'next':
        try:
            browser.find_element_by_xpath(x_path_next).click()
        except:
            flash('music: next failed')
    elif genre == 'off':
        try:
            browser.get('about:blank')
        except:
            flash('music: off failed')
    elif genre:
        try:
            if genre == 'random':
                _genre = choice(tuple(playlists.keys()))
                _pl = choice(playlists[_genre])
                browser.get(_pl)
            else:
                browser.get(choice(playlists[genre]))
            time.sleep(2)
            browser.find_element_by_xpath(x_path_menu).click()
            browser.find_element_by_xpath(x_path_radio).click()
        except Exception as e:
            print(e)
            try:
                time.sleep(5)
                browser.find_element_by_xpath(x_path_menu).click()
                browser.find_element_by_xpath(x_path_radio).click()
            except Exception as e:
                print(e)
                try:
                    browser.close()
                except:
                    pass
                del browser
                browser = None
                print('starte chrome neu')
                return redirect(url_for(f'{plugin_name}.music', genre=genre))
    return redirect(url_for('mainpage'))


@bp.route('/music')
def music_more():
    tiles = dict(
        # back=url_for('mainpage'),
        pop=url_for(f'{plugin_name}.music', genre='pop'),
        tropical_house=url_for(f'{plugin_name}.music', genre='tropical_house'),
        chill=url_for(f'{plugin_name}.music', genre='chill'),
        electroswing=url_for(f'{plugin_name}.music', genre='electroswing'),
        off=url_for(f'{plugin_name}.music', genre='off')
    )
    return render_template('scaffold.jinja2', tiles=tiles)
