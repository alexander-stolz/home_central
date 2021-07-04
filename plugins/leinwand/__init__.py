from flask import Blueprint, request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
import json
import serial
import time

plugin_name = 'leinwand'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            leinwand=dict(
                runter=url_for('{plugin_name}.leinwand', richtung='runter'),
                hoch=url_for('{plugin_name}.leinwand', richtung='hoch'),
            ),
        )"""

with open('plugins/leinwand/config.json') as config_file:
    config = json.load(config_file)
dev = serial.Serial(config.get('port'))

@bp.route('/screen/<richtung>')
def leinwand(richtung):
    if richtung == 'runter':
        dev.write(bytearray([0b11]))
    elif richtung == 'hoch':
        dev.write(bytearray([0b10]))
    elif richtung == 'pause':
        dev.write(bytearray([0b01]))
    return redirect(url_for('mainpage'))
