from flask import Blueprint
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect

plugin_name = 'system'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            system=dict(
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
    return redirect(url_for('mainpage'))
