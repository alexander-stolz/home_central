from flask import Blueprint
from flask.helpers import url_for
from werkzeug.utils import redirect
import json

plugin_name = 'ambicam'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            ambilight=dict(
                __default='#',
                start=url_for('{plugin_name}.start'),
                stop=url_for('{plugin_name}.stop'),
            ),
        )"""

with open(f'plugins/{plugin_name}/config.json') as config_file:
    config = json.load(config_file)


@bp.route('/ambicam/start')
def start():
    import urllib

    urllib.request.urlopen(f'http://{config["host"]}:{config["port"]}/start')
    return redirect(url_for('mainpage'))


@bp.route('/ambicam/stop')
def stop():
    import urllib

    urllib.request.urlopen(f'http://{config["host"]}:{config["port"]}/stop')
    return redirect(url_for('mainpage'))
