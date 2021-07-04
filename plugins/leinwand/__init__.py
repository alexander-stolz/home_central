from flask import Blueprint, request, flash
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
                __default=url_for('{plugin_name}.leinwand', richtung='status'),
                runter=url_for('{plugin_name}.leinwand', richtung='runter'),
                hoch=url_for('{plugin_name}.leinwand', richtung='hoch'),
            ),
        )"""

with open('plugins/leinwand/config.json') as config_file:
    config = json.load(config_file)
dev = serial.Serial(config.get('port'))

@bp.route('/screen/<richtung>')
def leinwand(richtung):
    global active
    if richtung == 'runter':
        dev.write(bytearray([0b11]))
    elif richtung == 'hoch':
        dev.write(bytearray([0b10]))
    elif richtung == 'status':
        # active = not active
        # while active:
        dev.write(bytearray([0b01]))
        time.sleep(.5)
        if dev.in_waiting:
            _pos = int(dev.readline().decode())
            _up = int(dev.readline().decode())
            _down = int(dev.readline().decode())
        flash(
            f'pos: {_pos}, {"not " if not (_up or _down) else ""}moving'
            f'{" up" if _up else ""}{" down" if _down else ""}'
            )
    return redirect(url_for('mainpage'))
