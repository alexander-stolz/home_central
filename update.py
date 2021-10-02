import subprocess
import platform

subprocess.run(['git', 'pull'])

try:
    open('lockfile', 'r')
    print('updating..')
    if platform.system() == 'Windows':
        subprocess.run(['python', '-m', 'pipenv', 'sync'])
    elif platform.system() == 'Linux':
        subprocess.run(['python3', '-m', 'pipenv', 'sync'])
except FileNotFoundError:
    open('lockfile', 'w').close()
