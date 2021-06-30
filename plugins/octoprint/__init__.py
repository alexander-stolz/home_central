from flask import Blueprint, flash
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from importlib import reload
import time

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
    try:
        from . import octoprint
    except OSError:
        flash('octoprint is not reachable')
        return redirect(url_for('mainpage'))
    except Exception as e:
        flash(e)
        return redirect(url_for('mainpage'))
    try:
        if cmd == 'cancel':
            octoprint.cancel()
        elif cmd == 'pause_resume':
            octoprint.pause_resume()
        elif cmd == 'move_up':
            octoprint.send_gcode('G1 Z100')
        elif cmd == 'home':
            octoprint.send_gcode('G28')
        elif cmd == 'disable_steppers':
            octoprint.send_gcode('M18 X Y')
        elif cmd == 'bed_heat':
            octoprint.heat_bed(65)
        elif cmd == 'bed_off':
            octoprint.heat_bed(0)
        elif cmd == 'tool_heat':
            octoprint.heat_extruder(215)
        elif cmd == 'tool_off':
            octoprint.heat_extruder(0)
        elif cmd == 'status':
            etl = octoprint.get_etl()
            etl = time.strftime('%H:%M:%S', time.gmtime(etl))
            flash(f'etl: {etl} ({octoprint.get_progress():.1f} %)')
        else:
            return cmd + ' not yet implemented'
    except Exception as e:
        print(e)
        print('reloading octoprint')
        reload(octoprint)
    return redirect(url_for('mainpage'))


@bp.route('/ender')
def ender_more():
    tiles = dict(
        back=url_for('mainpage'),
        control=dict(
            control=dict(
                cancel=url_for(f'{plugin_name}.ender', cmd='cancel'),
                pause=url_for(f'{plugin_name}.ender', cmd='pause_resume'),
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
        ),
        disable_steppers=url_for(f'{plugin_name}.ender', cmd='disable_steppers'),
        print_status=url_for(f'{plugin_name}.ender', cmd='status'),
    )
    return render_template('scaffold.jinja2', tiles=tiles)