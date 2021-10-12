from flask import Blueprint, request
from flask.templating import render_template
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
        elif res.get('type') == 'left':
            keyboard.press(Key.left)
            keyboard.release(Key.left)
        elif res.get('type') == 'space':
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        elif res.get('type') == 'f':
            keyboard.press('f')
            keyboard.release('f')
        elif res.get('type') == 'right':
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        elif res.get('type') == 'volume':
            if res['volume'] == '+':
                keyboard.press(Key.media_volume_up)
                keyboard.release(Key.media_volume_up)
            elif res['volume'] == '-':
                keyboard.press(Key.media_volume_down)
                keyboard.release(Key.media_volume_down)
        elif res.get('type') == 'key':
            _key = res['key']
            _ctrl = res['ctrl']
            if _ctrl:
                keyboard.press(Key.ctrl)
            keyboard.press(_key)
            keyboard.release(_key)
            if _ctrl:
                keyboard.release(Key.ctrl)
        elif res.get('type') == 'mouse':
            mouse.position = (res['x'], res['y'])
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
        return (json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'
        })
    return render_template('airmouse/airmouse.html')