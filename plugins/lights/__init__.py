from flask import Blueprint, request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from selenium import webdriver
import json
from random import choice
import time
import requests

plugin_name = 'licht'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            licht=dict(
                __default=url_for('{plugin_name}.licht_more'),
                _1=url_for(f'{plugin_name}.licht', bulb='wohnzimmer'),
                _2=url_for(f'{plugin_name}.licht', bulb='flur'),
                _3=url_for(f'{plugin_name}.licht', bulb='schlafzimmer'),
                all=url_for('{plugin_name}.licht', bulb='all'),
            )
        )"""

with open('plugins/lights/config.json') as config:
    KEY = json.load(config).get('apikey')
TEMPLATE = "https://maker.ifttt.com/trigger/{trigger}/with/key/{key}"


@bp.route('/light/<bulb>')
def licht(bulb:str=None):
    if bulb in ('wohnzimmer', 'all'):
        requests.get(TEMPLATE.format(trigger='LightsWohnzimmer', key=KEY))
    if bulb in ('flur', 'all'):
        requests.get(TEMPLATE.format(trigger='LightsFlur', key=KEY))
    if bulb in ('schlafzimmer', 'all'):
        requests.get(TEMPLATE.format(trigger='LightsSchlafzimmer', key=KEY))
    return redirect(url_for('mainpage'))


@bp.route('/light')
def licht_more():
    tiles = dict(
        back=url_for('mainpage'),
        wohnzimmer=url_for(f'{plugin_name}.licht', bulb='wohnzimmer'),
        flur=url_for(f'{plugin_name}.licht', bulb='flur'),
        schlafzimmer=url_for(f'{plugin_name}.licht', bulb='schlafzimmer'),
    )
    return render_template('scaffold.jinja2', tiles=tiles)
