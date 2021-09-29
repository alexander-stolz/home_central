git pull
python -m pipenv sync
python -m pipenv run hypercorn app:asgi_app --bind '0.0.0.0:5000'