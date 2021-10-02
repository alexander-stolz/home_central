from os import remove
from flask import Blueprint, flash, request, send_from_directory
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename
from datetime import datetime

plugin_name = 'system'
bp = Blueprint(plugin_name, __name__, template_folder='templates')

tile = f"""dict(
            system=dict(
                __default=url_for('{plugin_name}.system_more'),
                shutdown=url_for('{plugin_name}.system', cmd='shutdown'),
                cancel=url_for('{plugin_name}.system', cmd='cancel')
            ),
        )"""

UPLOADS = []


@bp.route('/system/<cmd>', methods=['GET', 'POST'])
def system(cmd):
    import os
    if cmd == 'shutdown':
        remove('lockfile')
        os.system('shutdown -s -t 10')
    if cmd == 'restart':
        remove('lockfile')
        os.system('shutdown -r -t 00')
    elif cmd == 'cancel':
        open('lockfile', 'w').close()
        os.system('shutdown -a')
    elif cmd == 'speedtest':
        import speedtest
        s = speedtest.Speedtest()
        flash(f'down: {s.download() / 1e6:.2f} mbit')
        flash(f'up: {s.upload() / 1e6:.2f} mbit')
    elif cmd == 'upload':
        file = request.files['file']
        filename_orig = file.filename
        filename_save = datetime.now().strftime(
            '%Y%m%d%H%M%S') + '_' + filename_orig
        filename_save = secure_filename(filename_save)
        file.save(f'./static/{filename_save}')
        UPLOADS.append((filename_orig, filename_save))
    elif cmd == 'download':
        return send_from_directory('./static',
                                   UPLOADS[-1][1],
                                   as_attachment=True,
                                   attachment_filename=UPLOADS[-1][0])

    return redirect(url_for('mainpage'))


@bp.route('/system')
def system_more():
    tiles = dict(__10235=url_for('mainpage'),
                 speedtest=url_for(f'{plugin_name}.system', cmd='speedtest'),
                 restart=url_for(f'{plugin_name}.system', cmd='restart'),
                 share=dict(share=dict(
                     send='#',
                     receive=url_for(f'{plugin_name}.system', cmd='download'),
                 )))
    return render_template('scaffold.jinja2',
                           tiles=tiles,
                           additional_footer=additional_footer)


additional_footer = """
<form id="upload-form" action="system/upload" method="post" enctype="multipart/form-data">
    <input id="file-input" type="file" name="file" style="display: none;" />
    <input id="file-submit" type="submit" name="submit" style="display: none;" />
</form>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
    $('#send').on('click', function() {
        $('#file-input').trigger('click');
    });
    $('#file-input').on('change', function() {
        $('#file-submit').trigger('click');
    });

</script>
"""