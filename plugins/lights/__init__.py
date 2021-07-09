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
from yeelight import Bulb
from kasa import SmartPlug
import asyncio

plugin_name = 'licht'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            licht=dict(
                __default=url_for('{plugin_name}.licht_more'),
                _1=url_for(f'{plugin_name}.licht', bulb='wohnzimmer', mainpage=True),
                _2=url_for(f'{plugin_name}.licht', bulb='esszimmer', mainpage=True),
                _3=url_for(f'{plugin_name}.licht', bulb='flur', mainpage=True),
                all=url_for('{plugin_name}.licht', bulb='all', mainpage=True),
            )
        )"""

with open('plugins/lights/config.json') as config_file:
    config = json.load(config_file)
    _key = config.get('ifttt').get('apikey', '')
    _user = config.get('sonoff').get('user')
    _pass = config.get('sonoff').get('password')
    _region = config.get('sonoff').get('region')
    _y_bulbs = config.get('yeelight').get('bulbs')
    _k_plugs = config.get('kasa').get('plugs')
IFTTT_TEMPLATE = "https://maker.ifttt.com/trigger/{trigger}/with/key/" + _key

s_connection = sonoff.Sonoff(_user, _pass, _region)
s_device_ids = {d['name']:d.get('deviceid') for d in s_connection.get_devices()}

s_devices = {name:s_connection.get_device(dev_id) for name, dev_id in s_device_ids.items()}
y_devices = {name:Bulb(ip) for name, ip in _y_bulbs.items()}
k_devices = {name:SmartPlug(ip) for name, ip in _k_plugs.items()}


def ifttt(trigger):
    requests.get(IFTTT_TEMPLATE.format(trigger=trigger))


def sonoff(device, state='toggle'):
    if state == 'toggle':
        d = s_devices[device]
        state = d['params']['switch']
        state = {'on':'off', 'off':'on'}[state]
    s_connection.switch(state, s_device_ids[device])
    time.sleep(.5)


def yeelight(device, state='toggle'):
    if state == 'toggle':
        y_devices[device].toggle()
    elif state == 'on':
        y_devices[device].turn_on()
    elif state == 'off':
        y_devices[device].turn_off()
    time.sleep(.5)


def kasa(device, state='toggle'):
    dev = k_devices[device]
    asyncio.run(dev.update())
    if state == 'toggle':
        state = 'on' if dev.is_off else 'off'
    if state == 'on':
        asyncio.run(dev.turn_on())
    elif state == 'off':
        asyncio.run(dev.turn_off())
    time.sleep(.5)


@bp.route('/light/<bulb>')
def licht(bulb:str=None):
    if bulb in ('flur', 'all'):
        yeelight('flur')
    if bulb in ('schlafzimmer', 'all'):
        yeelight('schlafzimmer')
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
    if bulb in ('wohnzimmer_decke', 'all'):
        yeelight('wohnzimmer')
    if bulb in ('globus', 'all'):
        kasa('globus')
    if bulb in ('baum', 'all'):
        kasa('baum')
    if bulb in ('wohnzimmer'):
        yeelight('wohnzimmer')
        kasa('globus')
        kasa('baum')
    if request.args.get('mainpage'):
        return redirect(url_for('mainpage'))
    return redirect(url_for(f'{plugin_name}.licht_more'))


@bp.route('/light')
def licht_more():
    tiles = dict(
        back=url_for('mainpage'),
        wohnzimmer=dict(
            _w=dict(
                __default=url_for(f'{plugin_name}.licht', bulb='wohnzimmer'),
                decke=url_for(f'{plugin_name}.licht', bulb='wohnzimmer_decke'),
                globus=url_for(f'{plugin_name}.licht', bulb='globus'),
                baum=url_for(f'{plugin_name}.licht', bulb='baum'),
            ),
        ),
        esszimmer=dict(
            _e=dict(
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
