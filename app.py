from types import SimpleNamespace
from typing import OrderedDict
from flask import Flask
from flask.templating import render_template
from flask.helpers import url_for
from importlib import import_module

app = Flask(__name__)

_plugins = [
    'airmouse',
    'music',
    'volume',
    'lights',
    'prismatik',
    'octoprint',
    'system'
]

# register plugins
modules = []
for plugin in _plugins:
    p = import_module(f'plugins.{plugin}')
    app.register_blueprint(p.bp)
    modules.append(p)

@app.route('/')
def mainpage():
    tiles = OrderedDict()
    for p in modules:
        tiles[p.plugin_name] = eval(p.tile)
    return render_template('scaffold.jinja2', tiles=tiles)

# python -m pipenv run flask run
if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=False)
