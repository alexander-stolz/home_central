from flask import Blueprint
from flask.helpers import url_for
import pynput
from os import system
import time

from werkzeug.utils import redirect

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()
# blocked_until = 0

plugin_name = 'netflix'
bp = Blueprint(plugin_name, __name__, template_folder='templates')

tile = f"""dict(
    netflix=dict(
        __default=url_for('{plugin_name}.netflix', cmd='open'),
        max=url_for('{plugin_name}.netflix', cmd='max'),
        captions=url_for('{plugin_name}.netfix', cmd='captions'),
        __9199=url_for('{plugin_name}.netflix', cmd='pause'),
    ),
)"""


@bp.get('/netflix/<cmd>')
def netflix(cmd):
    if cmd == 'open':
        system('start Netflix:')
    elif cmd == 'max':
        mouse.position = (1812, 1008)
        mouse.scroll(0, 10)
        time.sleep(0.5)
        mouse.click()
    elif cmd == 'captions':
        mouse.position = (1812, 30)
        mouse.scroll(0, 10)
        time.sleep(0.5)
        mouse.click()
        mouse.position = (996, 103)
        time.sleep(0.2)
        mouse.click()
    elif cmd == 'pause':
        keyboard.press('space')
        keyboard.release('space')
    return redirect(url_for('mainpage'))
