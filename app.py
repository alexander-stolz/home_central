from types import SimpleNamespace
from typing import OrderedDict
from flask import Flask
from flask.templating import render_template
from flask.helpers import url_for

app = Flask(__name__)

_plugins = [
    'airmouse',
    'volume',
    'music',
    'prismatik',
    'octoprint',
    'system'
]

# register plugins
for plugin in _plugins:
    exec(f'from plugins.{plugin}.plugin import bp; app.register_blueprint(bp)')

@app.route('/')
def mainpage():
    tiles = OrderedDict()
    for plugin in _plugins:
        exec(f'from plugins.{plugin}.plugin import plugin_name, tile; tiles[plugin_name] = eval(tile)')
    return render_template('scaffold.jinja2', tiles=tiles)

# python -m pipenv run flask run
if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=False)
