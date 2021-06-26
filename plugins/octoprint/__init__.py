from flask import Blueprint
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect

plugin_name = 'ender'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
    ender=dict(
        __default=url_for('{plugin_name}.ender_more'),
        home=url_for('{plugin_name}.ender', cmd='home'),
        up=url_for('{plugin_name}.ender', cmd='move_up'),
        cancel=url_for('{plugin_name}.ender', cmd='cancel'),
    ),
)"""

@bp.route('/ender/<cmd>')
def ender(cmd):
    from . import octoprint
    if cmd == 'cancel':
        octoprint.cancel()
    elif cmd == 'move_up':
        octoprint.send_gcode('G1 Z100')
    elif cmd == 'home':
        octoprint.send_gcode('G28')
    else:
        return cmd + ' not yet implemented'
    return redirect(url_for('mainpage'))


@bp.route('/ender')
def ender_more():
    tiles = dict(
        back=url_for('mainpage'),
        control=dict(
            control=dict(
                cancel=url_for(f'{plugin_name}.ender', cmd='cancel'),
                pause=url_for(f'{plugin_name}.ender', cmd='pause'),
                up=url_for(f'{plugin_name}.ender', cmd='move_up'),
            ),
        ),
        bed=dict(
            bed=dict(
                heat=url_for(f'{plugin_name}.ender', cmd='bed_heat'),
                off=url_for(f'{plugin_name}.ender', cmd='bed_off'),
            )
        ),
        tool=dict(
            tool=dict(
                heat=url_for(f'{plugin_name}.ender', cmd='tool_heat'),
                off=url_for(f'{plugin_name}.ender', cmd='tool_off'),
            ),
        )
    )
    return render_template('scaffold.jinja2', tiles=tiles)