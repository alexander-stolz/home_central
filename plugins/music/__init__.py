from flask import Blueprint, request, flash
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

with open('plugins/music/config.json') as config_file:
    config = json.load(config_file)

browser_opt = Options()
extensions = config.get('extensions', [])
for ext in extensions:
    browser_opt.add_extension(ext)

x_path_menu = '/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-browse-response/div[2]/ytmusic-detail-header-renderer/div/ytmusic-menu-renderer/tp-yt-paper-icon-button/tp-yt-iron-icon'
x_path_radio = '/html/body/ytmusic-app/ytmusic-popup-container/tp-yt-iron-dropdown/div/ytmusic-menu-popup-renderer/tp-yt-paper-listbox/ytmusic-menu-navigation-item-renderer[1]/a/yt-formatted-string'
x_path_playpause = '/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[2]/tp-yt-iron-icon'
x_path_next = '/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[3]/tp-yt-iron-icon'

search_template = 'https://music.youtube.com/search?q={}'
x_path_top_result = '/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[1]/div[2]'
x_path_top_menu = '/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[1]/div[2]/ytmusic-responsive-list-item-renderer/ytmusic-menu-renderer/tp-yt-paper-icon-button/tp-yt-iron-icon'
x_path_top_radio = '/html/body/ytmusic-app/ytmusic-popup-container/tp-yt-iron-dropdown/div/ytmusic-menu-popup-renderer/tp-yt-paper-listbox/ytmusic-menu-navigation-item-renderer[1]/a/yt-formatted-string'

@bp.route('/music/<genre>', methods=['GET', 'POST'])
def music(genre:str=None):
    def restart_browser(browser=None):
        if browser:
            browser.quit()
        browser = webdriver.Chrome(chrome_options=browser_opt)
        browser.create_options()
        browser.implicitly_wait(5)
        return browser

    global browser
    if browser:
        try:
            browser.execute_script("window.onbeforeunload = null;")
            browser.execute_script("window.alert = null;")
            browser.find_element_by_xpath(x_path_playpause).click()
        except:
            pass

    browser = browser or restart_browser()
    if request.method == 'GET':
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
                # time.sleep(2)
                browser.find_element_by_xpath(x_path_menu).click()
                browser.find_element_by_xpath(x_path_radio).click()
            except Exception as e:
                print(e)
                try:
                    time.sleep(5)
                    browser.find_element_by_xpath(x_path_menu).click()
                    browser.find_element_by_xpath(x_path_radio).click()
                except Exception as e:
                    browser = restart_browser(browser)
                    return redirect(url_for(f'{plugin_name}.music', genre=genre))
    elif request.method == 'POST':
        try:
            txt = request.form.get('text')
            search = '+'.join(txt.split())
            browser.get(search_template.format(search))
            # time.sleep(3)
            browser.find_element_by_xpath(x_path_top_result).click()
            browser.find_element_by_xpath(x_path_top_menu).click()
            browser.find_element_by_xpath(x_path_top_radio).click()
        except Exception as e:
            flash(str(e) + ' - try again')
            browser = restart_browser(browser)
    return redirect(url_for('mainpage'))


@bp.route('/music')
def music_more():
    tiles = dict(
        __10235=url_for('mainpage'),
        pop=url_for(f'{plugin_name}.music', genre='pop'),
        tropical_house=url_for(f'{plugin_name}.music', genre='tropical_house'),
        chill=url_for(f'{plugin_name}.music', genre='chill'),
        electroswing=url_for(f'{plugin_name}.music', genre='electroswing'),
        off=url_for(f'{plugin_name}.music', genre='off')
    )
    return render_template('scaffold.jinja2', tiles=tiles, additional_tile=wish_tile)

wish_tile = f"""
<form class="btn-group" style="display:flex" action="/music/search" method="POST">
<input
    type="text" id="txt" name="text" autocomplete="off" class="form-control"
    placeholder="make a wish" style="text-align: center; width: 100%;">
<button type="submit" class="btn btn-primary" style="width:5em;">send</button>
</form>
"""