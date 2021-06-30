from flask import Blueprint, request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
import json
import time
import pynput
from pynput.keyboard import Key
from pynput.mouse import Button

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()
blocked_until = 0

plugin_name = 'air_mouse'
bp = Blueprint(plugin_name, __name__, template_folder='templates')

tile = f"url_for('{plugin_name}.airmouse')"


@bp.route('/airmouse', methods=['GET', 'POST'])
def airmouse():
    def block_mouse(dt):
        global blocked_until
        blocked_until = time.perf_counter() + dt

    def mouse_blocked():
        return time.perf_counter() < blocked_until

    if request.method == 'POST':
        res = json.loads(request.get_data())
        if res.get('type') == 'enter':
            text = res.get('text')
            if text:
                keyboard.type(text)
            else:
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
        elif res.get('type') == 'del':
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
        else:
            dx, dy, touches = res['x'], res['y'], res['touches']
            if dx == dy == 0 and not mouse_blocked():
                if touches == 0:
                    mouse.click(Button.left)
                elif touches == 1:
                    mouse.click(Button.right)
            elif touches == 1 and not mouse_blocked():
                mouse.move(dx * 5, dy * 5)
            elif touches == 2:
                if abs(dx) > 2 > abs(dy) * 1:
                    mouse.scroll(dx, 0)
                elif abs(dy) > abs(dx) * 1:
                    mouse.scroll(0, dy / 3)
                block_mouse(dt=.3)
                # else:
                #     mouse.scroll(dx, dy)
        return (
            json.dumps({'success':True}),
            200,
            {'ContentType':'application/json'}
        )
    return render_template('airmouse/airmouse.html')