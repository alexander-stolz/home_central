"""
https://docs.octoprint.org/en/master/api/printer.html
"""

import requests
import logging
from json import load as load_config

log = logging.getLogger('octoprint control')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)
log.setLevel(logging.INFO)

with open('plugins/octoprint/config.json') as config_file:
    config = load_config(config_file)
    api_key = config['apikey']
    url = config.get('url') or 'http://ender.local/api/'

session = requests.Session()
session.headers.update({'X-Api-Key': api_key,
                        'Content-Type': 'application/json'})


def get(target):
    res = session.get(url + target)
    if res.ok:
        log.debug('%s (%s) %s', target, res.status_code, res.text)
        return res.json()
    else:
        log.warning('%s (%s) %s', target, res.status_code, res.text)


def post(target, json):
    res = session.post(url + target, json=json)
    log.debug('%s (%s) %s', target, res.status_code, res.text)


def status():
    return get('printer')


def heat_bed(temp):
    post('printer/bed', {'command': 'target', 'target': temp})


def get_bed_temp():
    return get('printer/bed')['bed']['actual']


def heat_extruder(temp):
    post('printer/tool', {'command': 'target', 'targets': {'tool0': temp}})


def get_extruder_temp():
    return get('printer/tool')['tool0']['actual']


def pause_resume():
    post('job', {'command': 'pause'})


def cancel():
    post('job', {'command': 'cancel'})


def get_progress():
    return get('job')['progress']['completion']


def get_etl():
    return get('job')['progress']['printTimeLeft']


def send_gcode(gcode):
    if len(gcode.split('\n')) > 1:
        post('printer/command', {'commands': gcode.split('\n')})
    else:
        post('printer/command', {'command': gcode})


def go_home():
    gcode = """
    G1 E-5 F3600
    G1 X220 Y220 Z10
    G1 E5
    """
    send_gcode(gcode)


def close():
    session.close()


try:
    sts = status()
    print(sts['state']['text'])
    print('bed:', sts['temperature']['bed'])
    print('tool:', sts['temperature']['tool0'])
except TypeError:
    print('printer not connected')
