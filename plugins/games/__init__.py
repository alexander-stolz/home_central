from flask import Blueprint, request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
import json
import time

plugin_name = 'games'
bp = Blueprint(plugin_name, __name__, template_folder='templates')

tile = f"url_for('{plugin_name}.games_more')"


@bp.route('/games/<game>')
def games(game):
    if game == 'snake':
        return render_template('games/snake.html')


@bp.route('/games')
def games_more():
    tiles = dict(
        __10235=url_for('mainpage'),
        snake=url_for(f'{plugin_name}.games', game='snake'),
    )
    return render_template('scaffold.jinja2', tiles=tiles)