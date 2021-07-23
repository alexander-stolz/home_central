from flask import Blueprint
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect

plugin_name = 'prismatik'
bp = Blueprint(plugin_name, __name__)

tile = f"""dict(
            ambilight=dict(
                __default='#',
                __127752=url_for('{plugin_name}.set_prismatik_profile', name='colour'),
                __128250=url_for('{plugin_name}.set_prismatik_profile', name='normal'),
            ),
        )"""

@bp.route('/prismatik/profile/<name>')
def set_prismatik_profile(name='colour'):
    import telnetlib
    with telnetlib.Telnet('192.168.1.108', '3636') as tn:
        tn.write(b'lock\n')
        tn.write(f'setprofile:{name}\n'.encode())
        tn.write(b'unlock\n')
        tn.write(b'exit\n')
    return redirect(url_for('mainpage'))
