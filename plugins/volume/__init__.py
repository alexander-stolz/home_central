from flask import Blueprint, request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
import pynput
from pynput.keyboard import Key

keyboard = pynput.keyboard.Controller()

plugin_name = 'volume'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            vol=dict(
                __default=url_for('{plugin_name}.volume', volume='toggle_mute'),
                leiser=url_for('{plugin_name}.volume', volume='-'),
                lauter=url_for('{plugin_name}.volume', volume='+'),
            ),
        )"""


@bp.route('/volume/<volume>')
def volume(volume:str=None):
    # default = toggle mute
    if volume == '+':
        for _ in range(2):
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
    elif volume == '-':
        for _ in range(2):
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
    else:
        # toggle
        keyboard.press(Key.media_volume_mute)
        keyboard.release(Key.media_volume_mute)
    return redirect(url_for('mainpage'))
