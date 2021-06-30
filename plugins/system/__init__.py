from flask import Blueprint, flash
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect

plugin_name = 'system'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            system=dict(
                __default=url_for('{plugin_name}.system_more'),
                shutdown=url_for('{plugin_name}.system', cmd='shutdown'),
                cancel=url_for('{plugin_name}.system', cmd='cancel')
            ),
        )"""

@bp.route('/system/<cmd>')
def system(cmd):
    import os
    if cmd == 'shutdown':
        os.system('shutdown -s -t 10')
    elif cmd == 'cancel':
        os.system('shutdown -a')
    elif cmd == 'speedtest':
        import speedtest
        s = speedtest.Speedtest()
        flash(f'down: {s.download() / 1e6:.2f} mbit')
        flash(f'up: {s.upload() / 1e6:.2f} mbit')
    return redirect(url_for('mainpage'))


@bp.route('/system')
def system_more():
    tiles = dict(
        speedtest=url_for(f'{plugin_name}.system', cmd='speedtest')
    )
    return render_template('scaffold.jinja2', tiles=tiles)
