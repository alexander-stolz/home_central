from flask import Blueprint, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
import json
import urllib

plugin_name = 'ambicam'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            ambicam=dict(
                __default='#',
                start=url_for('{plugin_name}.start'),
                stop=url_for('{plugin_name}.stop'),
            ),
        )"""

with open(f'plugins/{plugin_name}/config.json') as config_file:
    config = json.load(config_file)


@bp.route('/ambicam/start')
def start():
    urllib.request.urlopen(f'http://{config["host"]}:{config["port"]}/start/force')
    return redirect(url_for('mainpage'))


@bp.route('/ambicam/stop')
def stop():
    urllib.request.urlopen(f'http://{config["host"]}:{config["port"]}/stop')
    return redirect(url_for('mainpage'))


@bp.route('/ambicam_color/<cmd>')
def ambicam_color(cmd):
    urllib.request.urlopen(f'http://{config["host"]}:{config["port"]}/color/{cmd}')
    return redirect(url_for(f'{plugin_name}.ambicam_more'))


@bp.route('/ambicam')
def ambicam_more():
    tiles = dict(
        __10235=url_for('mainpage'),
        auto_colors=url_for(f'{plugin_name}.ambicam_color', cmd='auto_colors'),
        red=dict(
            red=dict(
                __8722=url_for(f'{plugin_name}.ambicam_color', cmd='red_down'),
                __43=url_for(f'{plugin_name}.ambicam_color', cmd='red_up'),
            ),
        ),
        green=dict(
            green=dict(
                __8722=url_for(f'{plugin_name}.ambicam_color', cmd='green_down'),
                __43=url_for(f'{plugin_name}.ambicam_color', cmd='green_up'),
            ),
        ),
        blue=dict(
            blue=dict(
                __8722=url_for(f'{plugin_name}.ambicam_color', cmd='blue_down'),
                __43=url_for(f'{plugin_name}.ambicam_color', cmd='blue_up'),
            ),
        ),
        brightness=dict(
            brightness=dict(
                __8722=url_for(f'{plugin_name}.ambicam_color', cmd='brightness_down'),
                __43=url_for(f'{plugin_name}.ambicam_color', cmd='brightness_up'),
            ),
        ),
    )
    return render_template('scaffold.jinja2', tiles=tiles)
