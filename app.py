# https://www.youtube.com/watch?v=sFsRylCQblw
import json
from typing import OrderedDict
from flask import Flask
from flask.helpers import url_for
from flask.templating import render_template
from importlib import import_module
from asgiref.wsgi import WsgiToAsgi

with open('config.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.secret_key = config.get('secret_key', '1234')
asgi_app = WsgiToAsgi(app)

# register plugins
modules = []
for plugin in config.get('plugins', []):
    p = import_module(f'plugins.{plugin}')
    app.register_blueprint(p.bp)
    modules.append(p)
    print(f'[x] Registered plugin {plugin}')


@app.route('/')
def mainpage():
    tiles = OrderedDict()
    for p in modules:
        tiles[p.plugin_name] = eval(p.tile)
    return render_template('scaffold.jinja2', tiles=tiles)


# python -m pipenv run flask run
if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=config.get('debug', False))
