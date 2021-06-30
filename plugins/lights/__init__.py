from flask import Blueprint, request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from selenium import webdriver
import json
from random import choice
import time
import requests
from . import sonoff

plugin_name = 'licht'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            licht=dict(
                __default=url_for('{plugin_name}.licht_more'),
                _1=url_for(f'{plugin_name}.licht', bulb='wohnzimmer'),
                _2=url_for(f'{plugin_name}.licht', bulb='esszimmer'),
                _3=url_for(f'{plugin_name}.licht', bulb='flur'),
                all=url_for('{plugin_name}.licht', bulb='all'),
            )
        )"""

with open('plugins/lights/config.json') as config_file:
    config = json.load(config_file)
    _key = config.get('yeelight').get('apikey')
    _user = config.get('sonoff').get('user')
    _pass = config.get('sonoff').get('password')
    _region = config.get('sonoff').get('region')
Y_TEMPLATE = "https://maker.ifttt.com/trigger/{trigger}/with/key/" + _key

s_connection = sonoff.Sonoff(_user, _pass, _region)
s_device_ids = {d['name']:d.get('deviceid') for d in s_connection.get_devices()}
print(s_device_ids)

def yeelight(trigger):
    requests.get(Y_TEMPLATE.format(trigger=trigger))


def sonoff(device, state='toggle'):
    if state == 'toggle':
        d = s_connection.get_device(s_device_ids[device])
        state = d['params']['switch']
        state = {'on':'off', 'off':'on'}[state]
    s_connection.switch(state, s_device_ids[device])
    time.sleep(.5)


@bp.route('/light/<bulb>')
def licht(bulb:str=None):
    if bulb in ('wohnzimmer', 'all'):
        yeelight('LightsWohnzimmer')
    if bulb in ('flur', 'all'):
        yeelight('LightsFlur')
    if bulb in ('schlafzimmer', 'all'):
        yeelight('LightsSchlafzimmer')
    if bulb in ('esstisch', 'all'):
        sonoff('Esstisch')
    if bulb in ('ananas', 'all'):
        sonoff('Ananas')
    if bulb in ('bild', 'all'):
        sonoff('Bild')
    if bulb in ('schild', 'all'):
        sonoff('Schild')
    if bulb in ('esszimmer'):
        sonoff('Esstisch')
        sonoff('Bild')
        sonoff('Ananas')
    return redirect(url_for(f'{plugin_name}.licht_more'))


@bp.route('/light')
def licht_more():
    tiles = dict(
        back=url_for('mainpage'),
        wohnzimmer=url_for(f'{plugin_name}.licht', bulb='wohnzimmer'),
        esszimmer=dict(
            esszimmer=dict(
                __default=url_for(f'{plugin_name}.licht', bulb='esszimmer'),
                tisch=url_for(f'{plugin_name}.licht', bulb='esstisch'),
                bild=url_for(f'{plugin_name}.licht', bulb='bild'),
                tv=url_for(f'{plugin_name}.licht', bulb='ananas'),
            ),
        ),
        flur=url_for(f'{plugin_name}.licht', bulb='flur'),
        schild=url_for(f'{plugin_name}.licht', bulb='schild'),
        schlafzimmer=url_for(f'{plugin_name}.licht', bulb='schlafzimmer'),
    )
    return render_template('scaffold.jinja2', tiles=tiles)
